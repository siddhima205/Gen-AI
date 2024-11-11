import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from ollama import Ollama

normal_data = pd.read_csv("normal_data.csv")
faulty_data = pd.read_csv("faulty_data.csv")

normal_data["label"] = "normal"
faulty_data["label"] = "faulty"

combined_data = pd.concat([normal_data, faulty_data])

combined_data["timestamp"] = pd.to_datetime(combined_data["timestamp"])
combined_data["hour"] = combined_data["timestamp"].dt.hour
combined_data["day"] = combined_data["timestamp"].dt.day
combined_data["month"] = combined_data["timestamp"].dt.month
combined_data["year"] = combined_data["timestamp"].dt.year

scaler = StandardScaler()
combined_data[["sensor1", "sensor2", "sensor3"]] = scaler.fit_transform(combined_data[["sensor1", "sensor2", "sensor3"]])

X = combined_data.drop(columns=["label", "timestamp"])
y = combined_data["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Ollama.load_model("llama3")

def convert_to_text(row):
    return f"Sensor readings: Sensor1={row['sensor1']}, Sensor2={row['sensor2']}, Sensor3={row['sensor3']}, Hour={row['hour']}, Day={row['day']}, Label={row['label']}"

text_data = combined_data.apply(convert_to_text, axis=1)
model.fine_tune(text_data)

evaluation_results = model.evaluate(X_test, y_test)
print(evaluation_results)

model.save('operate_mark1')