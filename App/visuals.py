import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(file_path):
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")
    return data

def analyze_data(data):
    summary = {
        'columns': data.columns.tolist(),
        'dtypes': data.dtypes.tolist(),
        'shape': data.shape,
        'missing_values': data.isnull().sum().tolist()
    }
    return summary

def recommend_and_generate_visualizations(data):
    visualizations = []
    for column in data.columns:
        if pd.api.types.is_numeric_dtype(data[column]):
            plt.figure(figsize=(10, 6))
            sns.histplot(data[column], kde=True)
            plt.title(f'Distribution of {column}')
            filename = f'{column}_distribution.svg'
            plt.savefig(f'uploads/{filename}', format='svg')
            plt.close()
            visualizations.append(filename)
        elif pd.api.types.is_categorical_dtype(data[column]):
            plt.figure(figsize=(10, 6))
            sns.countplot(y=data[column])
            plt.title(f'Count of {column}')
            filename = f'{column}_count.svg'
            plt.savefig(f'uploads/{filename}', format='svg')
            plt.close()
            visualizations.append(filename)
    
    # Correlation heatmap for numeric features
    numeric_columns = data.select_dtypes(include='number').columns
    if len(numeric_columns) > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(data[numeric_columns].corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Heatmap')
        filename = 'correlation_heatmap.svg'
        plt.savefig(f'uploads/{filename}', format='svg')
        plt.close()
        visualizations.append(filename)
    
    return visualizations

def generate_visualizations_from_file(file_path):
    data = load_data(file_path)
    summary = analyze_data(data)
    print("Data Summary:")
    print(summary)
    
    visualizations = recommend_and_generate_visualizations(data)
    return visualizations
