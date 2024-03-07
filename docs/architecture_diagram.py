from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.compute import Functions
from diagrams.gcp.storage import Storage
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.security import KeyManagementService
from diagrams.gcp.operations import Monitoring
from diagrams.gcp.network import LoadBalancing

def create_architecture_diagram():
    with Diagram("Meeting Minutes Serverless Architecture", show=False, direction="LR"):
        with Cluster("GCP"):
            with Cluster("Cloud Storage"):
                audio_storage = Storage("Audio Files")
                transcription_storage = Storage("Transcriptions")
                minutes_storage = Storage("Meeting Minutes")
            
            with Cluster("Cloud Functions"):
                upload_func = Functions("Upload Audio")
                transcribe_func = Functions("Transcribe Audio")
                extract_func = Functions("Extract Minutes")
                generate_func = Functions("Generate Document")
            
            with Cluster("Pub/Sub"):
                transcription_topic = PubSub("Transcription Completed")
                minutes_topic = PubSub("Minutes Extracted")
            
            with Cluster("Secret Manager"):
                secrets = KeyManagementService("API Keys")
            
            with Cluster("Cloud Monitoring"):
                monitoring = Monitoring("Monitoring and Logging")
            
            with Cluster("Load Balancer"):
                load_balancer = LoadBalancing("HTTP Load Balancer")
            
        load_balancer >> Edge(color="darkgreen", style="bold") >> upload_func >> Edge(color="darkgreen", style="bold") >> audio_storage
        audio_storage >> Edge(color="darkgreen", style="bold", label="Triggers") >> transcribe_func >> Edge(color="darkgreen", style="bold") >> transcription_storage
        transcribe_func >> Edge(color="darkgreen", style="bold", label="Publishes") >> transcription_topic >> Edge(color="darkgreen", style="bold", label="Triggers") >> extract_func
        extract_func >> Edge(color="darkgreen", style="bold") >> minutes_storage
        extract_func >> Edge(color="darkgreen", style="bold", label="Publishes") >> minutes_topic >> Edge(color="darkgreen", style="bold", label="Triggers") >> generate_func >> Edge(color="darkgreen", style="bold") >> minutes_storage
        secrets >> Edge(color="darkblue", style="dashed") >> upload_func
        secrets >> Edge(color="darkblue", style="dashed") >> transcribe_func
        secrets >> Edge(color="darkblue", style="dashed") >> extract_func
        upload_func >> Edge(color="darkred", style="dashed") >> monitoring
        transcribe_func >> Edge(color="darkred", style="dashed") >> monitoring
        extract_func >> Edge(color="darkred", style="dashed") >> monitoring
        generate_func >> Edge(color="darkred", style="dashed") >> monitoring

if __name__ == "__main__":
    create_architecture_diagram()