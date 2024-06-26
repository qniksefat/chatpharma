import { Outlet, NavLink, Link } from "react-router-dom";

import padana from "../../assets/padana-white.svg";

import styles from "./Layout.module.css";

import { useLogin } from "../../authConfig";

import { LoginButton } from "../../components/LoginButton";

const Layout = () => {
    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer}>
                    <div className={styles.headerLeft}>
                        <Link to="/" className={styles.headerTitleContainer}>
                            <img src={padana} alt="GitHub logo" className={styles.headerLogo} />
                            <h3 className={styles.headerTitle}>Padana</h3>
                        </Link>
                    </div>
                    {useLogin && <LoginButton />}
                </div>
            </header>

            <Outlet />
        </div>
    );
};

export default Layout;
