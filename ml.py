import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

from scipy.stats import zscore
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_auc_score, accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

import warnings
warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv("plant_health_data_weighted.csv")

# Selecting relevant features and target variable
features = ["Soil_Moisture", "Ambient_Temperature", "Humidity", "Light_Intensity"]
# features = ["Ambient_Temperature"]
target = "Plant_Health_Status"

# Extract input features and target labels
X = df[features].values
y = df[target].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Display the shapes of the splits for verification
print("X_train Shape:", X_train.shape)
print("X_test Shape:", X_test.shape)
print("y_train Shape:", y_train.shape)
print("y_test Shape:", y_test.shape)

# Apply StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize models
models = {
    "KNN Classifier": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

# Display model names to confirm initialization
print("Models initialized:", list(models.keys()))

# Initialize lists to store results
results = []

# Train and evaluate each model
for model_name, model in models.items():
    # Train the model
    model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = model.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Calculate AUC
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test_scaled)
        auc = roc_auc_score(y_test, y_prob, multi_class='ovr')
    else:
        auc = None

    # Store results
    results.append({
        "Model": model_name,
        "Accuracy": accuracy,
        "AUC": auc,
        "Confusion Matrix": confusion_matrix(y_test, y_pred),
        "Classification Report": classification_report(y_test, y_pred, target_names=['Healthy', 'Moderate Stress', 'High Stress'])
    })

# Display results for each model
for result in results:
    print(f"\nModel: {result['Model']}")
    print(f"Accuracy: {result['Accuracy']:.2f}")
    if result["AUC"] is not None:
        print(f"AUC: {result['AUC']:.2f}")

    # Confusion Matrix Visualization
    cm = result["Confusion Matrix"]
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu', xticklabels=['Healthy', 'Moderate Stress', 'High Stress'],
                yticklabels=['Healthy', 'Moderate Stress', 'High Stress'])
    plt.title(f'Confusion Matrix for {result["Model"]}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    #plt.show()

    # Print Classification Report
    print(result["Classification Report"])

    # Prepare a summary table for model evaluation
evaluation_summary = []

# Extract the key metrics for each model
for result in results:
    evaluation_summary.append({
        "Model": result["Model"],
        "Accuracy": result["Accuracy"],
        "AUC": result["AUC"]
    })

evaluation_summary_df = pd.DataFrame(evaluation_summary)

# Sort by accuracy and display
display(evaluation_summary_df.sort_values(by="Accuracy", ascending=False))

# Select the Model with the Highest AUC
best_model_name = max(results, key=lambda x: x["AUC"] if x["AUC"] is not None else -1)["Model"]
best_model = models[best_model_name]
print(f"The best model based on AUC is: {best_model_name}")

# Generate Predictions
y_pred_best = best_model.predict(X_test_scaled)

# Plot the Distribution of Predictions
plt.figure(figsize=(8, 6))
sns.countplot(x=y_pred_best, palette='YlGnBu')
plt.xticks([0, 1, 2], labels=["Healthy", "Moderate Stress", "High Stress"])
plt.xlabel("Predicted Plant Health Status")
plt.ylabel("Count")
plt.title(f"Distribution of Predictions by {best_model_name}")
plt.tight_layout()
#plt.show()

plt.figure(figsize=(10, 6))

# Convert the actual and predicted values to a DataFrame for comparison
actual_vs_predicted = pd.DataFrame({
    'Actual': y_test,
    'Predicted': best_model.predict(X_test_scaled)
})

sns.countplot(
    data=actual_vs_predicted.melt(var_name='Type', value_name='Plant Health Status'),
    x='Plant Health Status', hue='Type', palette='YlGnBu'
)

plt.xticks([0, 1, 2], labels=["Healthy", "Moderate Stress", "High Stress"])
plt.xlabel("Plant Health Status")
plt.ylabel("Count")
plt.title("Actual vs Predicted Plant Health Status")
plt.legend(title="Type", loc="upper left")
plt.tight_layout()
#plt.show()

# Function to make predictions
def predict_health(soil_moisture, temp, humidity, lux):
    input_data = np.array([[soil_moisture, temp, humidity, lux]])
    input_scaled = scaler.transform(input_data)
    prediction = best_model.predict(input_scaled)
    return prediction

example = predict_health(32, 35, 50, 600)
print("Predicted Plant Health Status:", example)