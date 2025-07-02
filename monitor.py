import os
import time
import pandas as pd
from src.predict import predict_flows, predict_pcap
import joblib
import subprocess
import traceback
import sys

if len(sys.argv) < 2:
    print("usage: python monitor.py <network interface>")
    sys.exit(1)
interface=sys.argv[1]
temp_pcap_name='live_capture.pcap'
temp_pcap=os.path.join(os.path.expanduser("~"),temp_pcap_name)
capture_duration=10

label_encoder=joblib.load('results/label_encoder.pkl')
class_names=list(label_encoder.classes_)
benign_label_index=class_names.index('BENIGN') if 'BENIGN' in class_names else 0

print("🔍 Live Intrusion Detection Monitor Started...")
print(f"Capturing from interface: {interface}\n")

while True:
    try:
        print(f'⏺️ Capturing {capture_duration}s of traffic...')
        subprocess.run([
            "tcpdump",
            "-i", interface,
            "-w", temp_pcap,
            "-c", "100",
            "-nn",
            "-q"
        ])
        if not os.path.exists(temp_pcap):
            print(f"⚠️  Warning: {temp_pcap} not found. Skipping this cycle.")
            time.sleep(1)
            continue
        print('📊 Analyzing captured traffic...')

        try:
            results=predict_pcap(temp_pcap)
            malicious=results[results['prediction'] != 'BENIGN']
            if not malicious.empty:
                print("\n🚨 ALERT: Intrusion detected!")
                for _,row in malicious.iterrows():
                    label_name = row['prediction']
                    if label_name == "BENIGN":
                        continue 
                    print(f"⚠️ {row['source_ip']} → {row['dest_ip']} | Attack: {label_name} | Confidence: {row['confidence']:.2f}")
                print("")
            else:
                print("✅ No intrusion detected.")

        except Exception as e:
            print(f'Error:{str(e)}')
            traceback.print_exc()
        if os.path.exists(temp_pcap):
            os.remove(temp_pcap)

        time.sleep(1)
        
    except KeyboardInterrupt:
        print("🛑 Monitor stopped by user.")
        break