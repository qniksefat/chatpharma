#!/bin/sh

echo ""
echo "Loading azd .env file from current environment"
echo ""

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file"
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found"
fi

while IFS='=' read -r key value; do
    value=$(echo "$value" | sed 's/^"//' | sed 's/"$//')
    export "$key=$value"
done <<EOF
$(azd env get-values)
EOF

if not command -v azd &> /dev/null; then
    echo "azd command not found, skipping .env file load"
else
    if [ -z "$(azd env list | grep -w true | awk '{print $1}')" ]; then
        echo "No azd environments found, skipping .env file load"
    else
        echo "Loading azd .env file from current environment"
        while IFS='=' read -r key value; do
        value=$(echo "$value" | sed 's/^"//' | sed 's/"$//')
        export "$key=$value"
        done <<EOF
$(azd env get-values --no-prompt)
EOF
    fi
fi



cd ../
echo 'Creating python virtual environment ".venv"'
python3 -m venv .venv

echo ""
echo "Restoring backend python packages"
echo ""

./.venv/bin/python -m pip install -r app/backend/requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to restore backend python packages"
    exit $?
fi

echo ""
echo "Restoring frontend npm packages"
echo ""

cd app/frontend
npm install
if [ $? -ne 0 ]; then
    echo "Failed to restore frontend npm packages"
    exit $?
fi

echo ""
echo "Building frontend"
echo ""

npm run build
if [ $? -ne 0 ]; then
    echo "Failed to build frontend"
    exit $?
fi

echo ""
echo "Starting backend"
echo ""

cd ../backend

port=50505
host=localhost
../../.venv/bin/python -m quart --app main:app run --port "$port" --host "$host" --reload
if [ $? -ne 0 ]; then
    echo "Failed to start backend"
    exit $?
fi
