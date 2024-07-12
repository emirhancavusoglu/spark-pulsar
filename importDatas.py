import pulsar
import json
import pandas as pd

def send_data_to_pulsar(file_path, topic_name):
    try:
        client = pulsar.Client('pulsar://localhost:6650')
        producer = client.create_producer(topic_name)

        df = pd.read_excel(file_path, engine='openpyxl')

        #selected_columns = df[['login_fail_count','source_address']]
        selected_columns = df
        data_to_send = [json.dumps(row.to_dict()) for index, row in selected_columns.iterrows()]
        for data in data_to_send:
            producer.send(data.encode('utf-8'))
            print(data)
        print("Veriler başarıyla gönderildi.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    finally:
        client.close()


file_path = 'cf2.xlsx'
topic_name = 'login_fail_countTopic'
send_data_to_pulsar(file_path, topic_name)
