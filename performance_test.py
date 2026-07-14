import nest_asyncio
import asyncio
import websockets
import time
import statistics
import threading
import uvicorn
from fastapi import FastAPI, WebSocket

nest_asyncio.apply()
app = FastAPI()

@app.websocket("/ws/bio-signal")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Simulate real-time TDA execution overhead (0.032 ms)
            await asyncio.sleep(0.000032) 
            await websocket.send_text('{"status": "processed", "safety_flag": "CLEAR"}')
    except Exception:
        pass

def start_background_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

# Launch server daemon thread
server_thread = threading.Thread(target=start_background_server, daemon=True)
server_thread.start()
time.sleep(2) # Await server boot

async def measure_single_client(client_id, num_messages=50):
    uri = "ws://127.0.0.1:8000/ws/bio-signal"
    latencies = []
    try:
        async with websockets.connect(uri) as websocket:
            for _ in range(num_messages):
                start = time.perf_counter()
                await websocket.send('{"client_id": "' + client_id + '", "z_hat": 0.45}')
                await websocket.recv() 
                latencies.append((time.perf_counter() - start) * 1000)
                await asyncio.sleep(0.1) # 10Hz
    except Exception as e:
         print(f"Error on {client_id}: {e}")
    return latencies

async def run_stress_test(num_clients):
    print(f"\n--- RUNNING STRESS TEST WITH {num_clients} CONCURRENT DEVICES ---")
    tasks = [measure_single_client(f"Device_{i}") for i in range(num_clients)]
    results = await asyncio.gather(*tasks)
    all_latencies = [lat for res in results for lat in res]
    
    if all_latencies:
        print(f"Total packets processed: {len(all_latencies)}")
        print(f"Average Latency (RTT): {statistics.mean(all_latencies):.2f} ms")
        print(f"95th Percentile Latency (P95): {statistics.quantiles(all_latencies, n=100)[94]:.2f} ms")
        print(f"Maximum Latency (Max RTT): {max(all_latencies):.2f} ms")

async def main():
    for scale in [1, 10, 50]:
        await run_stress_test(scale)

asyncio.run(main())
