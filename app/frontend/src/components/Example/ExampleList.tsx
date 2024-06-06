import React from "react";
import { Example } from "./Example";
import styles from "./Example.module.css";

const DEFAULT_EXAMPLES: string[] = [
    "What ensures accurate drug effect measurement instruments?",
    "What factors affect local drug bioavailability in nose?",
    "What does a bridging study aim to provide?"
];

const GPT4V_EXAMPLES: string[] = [
    "Compare the impact of interest rates and GDP in financial markets.",
    "What is the expected trend for the S&P 500 index over the next five years? Compare it to the past S&P 500 performance",
    "Can you identify any correlation between oil prices and stock market trends?"
];

interface Props {
    onExampleClicked: (value: string, id?: string) => void;
    useGPT4V?: boolean;
    conversationId?: string;
}

export const ExampleList = ({ onExampleClicked, useGPT4V, conversationId }: Props) => {
    return (
        <ul className={styles.examplesNavList}>
            {(useGPT4V ? GPT4V_EXAMPLES : DEFAULT_EXAMPLES).map((question, i) => (
                <li key={i}>
                    <Example text={question} value={question} onClick={(value) => onExampleClicked(value, conversationId)} />
                </li>
            ))}
        </ul>
    );
};

