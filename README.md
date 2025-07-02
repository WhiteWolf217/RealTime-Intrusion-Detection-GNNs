# 🛡️ RealTime-Intrusion-Detection-GNNs

# 📦 Prerequisites & Installation
    System Requirements
      Python 3.10

# ✅ Features
    1. Captures live traffic using tcpdump
    2. Converts packet flows into graph format
    3. Uses a trained GNN model to predict attack labels
    4. Displays live alerts for suspicious flows

# 🧰 Prerequisites
  Ensure the following components are installed and configured:
  
    1. Python Packages (installed via requirements.txt)
          pip install -r requirements.txt
    2. System Tools
          tcpdump
          Root privileges to capture packets

# 🚀 Usage
        Basic Command
          sudo python monitor.py <network_interface>
        Example:
          sudo python monitor.py wlan0

    OR
        Via docker (no need for prerequisites then)
          Install by:
            docker push whitewolf217/realtime-gnn-intrusion-app:tagname
          Run by:
            sudo docker run \
            --net=host \
            --cap-add=NET_ADMIN \
            --cap-add=NET_RAW \
            -v $PWD/results:/app/results \
            --rm \
            realtime-gnn-intrusion-app <interface>
          
# 📌 How to Train with Your Own Data (not for docker)
    To train the model using your own dataset, follow these steps:

        1. Prepare your data: First, place the path to your training data within the data_processing_incremental.py script.
        2. Process the data: Run the data processing script: 'python data_processing_incremental.py'
        3. Train the model: After the data is processed, initiate training: 'python train_incremental.py'
        4. Finally, run sudo 'python monitor.py <network_interface>'
