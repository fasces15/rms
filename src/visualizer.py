import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
import pandas as pd

class Visualizer:
    @staticmethod
    def plot_error_distribution(error_counts: Dict[str, int], title: str):
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(error_counts.keys()), y=list(error_counts.values()))
        plt.title(title)
        plt.xlabel('Error Code')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt

    @staticmethod
    def plot_error_trend(error_trend: pd.Series, title: str):
        plt.figure(figsize=(12, 6))
        error_trend.plot(kind='line')
        plt.title(title)
        plt.xlabel('Hour of Day')
        plt.ylabel('Error Count')
        plt.tight_layout()
        return plt

    @staticmethod
    def plot_errors_by_category(error_dict: Dict[str, Dict[str, int]], title: str):
        fig, axes = plt.subplots(len(error_dict), 1, figsize=(12, 6*len(error_dict)))
        for (category, errors), ax in zip(error_dict.items(), axes.flatten() if len(error_dict) > 1 else [axes]):
            sns.barplot(x=list(errors.keys()), y=list(errors.values()), ax=ax)
            ax.set_title(f'{title}: {category}')
            ax.set_xlabel('Error Code')
            ax.set_ylabel('Count')
            ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        return plt