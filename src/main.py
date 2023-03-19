import asyncio
from fs22server import FS22ServerConfig
from servertracker import ServerTracker
from infopanelhandler import InfoPanelConfig, InfoPanelHandler
from dotenv import load_dotenv
import os
import signal
import sys

stopped = False


def initial(serverId, serverData):
    print("[main] Received initial event for server %s" % (serverId))


def updated(serverId, serverData):
    # print("[main]Received update event for server %s" % (serverId, serverData.__dict__))
    pass


def playerWentOnline(serverId, playerName):
    print("[main] Player %s joined server %s" % (playerName, serverId))


def playerWentOffline(serverId, playerName):
    print("[main] Player %s logged out from server %s" % (playerName, serverId))


def serverStatusChanged(serverId, serverData):
    print("[main] Server %s is now %s" % (serverId, serverData.status.name))


def playerAdminStateChanged(serverId, playerName):
    print("[main] Player %s is now an admin" % (playerName))


async def main():
    print("[main] Launching main")

    if os.path.exists("/data"):
        print("[main] /data exists")
    if os.path.exists("/data/storage"):
        print("[main] /data/storage exists")
    if os.path.exists("C:/temp"):
        print("[main] C:\\temp exists")

    if os.getenv("SERVER_A_IP") is None:
        print("[main] Loading local environment")
        load_dotenv()
    else:
        print("[main] Using existing environment")

    serverA = FS22ServerConfig(0, os.getenv("SERVER_A_IP"), os.getenv(
        "SERVER_A_PORT"), os.getenv("SERVER_A_APICODE"))
    serverB = FS22ServerConfig(1, os.getenv("SERVER_B_IP"), os.getenv(
        "SERVER_B_PORT"), os.getenv("SERVER_B_APICODE"))
    serverC = FS22ServerConfig(2, os.getenv("SERVER_C_IP"), os.getenv(
        "SERVER_C_PORT"), os.getenv("SERVER_C_APICODE"))
    serverD = FS22ServerConfig(3, os.getenv("SERVER_D_IP"), os.getenv(
        "SERVER_D_PORT"), os.getenv("SERVER_D_APICODE"))

    serverConfigs = [serverA, serverB, serverC, serverD]

    testConfig = InfoPanelConfig(os.getenv("SERVER_C_IP"), os.getenv("SERVER_C_PORT"), "tmp", "tmpTitle", "0", "1", "2", "blue")
    testHandler = InfoPanelHandler()
    testHandler.add_config(2, testConfig)

    for serverConfig in serverConfigs:
        tracker = ServerTracker(serverConfig)
        tracker.events.initial += initial
        tracker.events.initial += testHandler.on_initial_event
        tracker.events.updated += updated
        tracker.events.updated += testHandler.on_updated
        tracker.events.playerWentOnline += playerWentOnline
        tracker.events.playerWentOffline += playerWentOffline
        tracker.events.serverStatusChanged += serverStatusChanged
        tracker.events.playerAdminStateChanged += playerAdminStateChanged
        tracker.start_tracker()

    print("[main] Finished initialization")
    testHandler.start()

    while (not stopped):
        print("[main] Sleeping 60s", flush=True)
        await asyncio.sleep(60)

    print("[main] Waiting for threads to end")
    testHandler.stop()
    print("[main] Done")


def signal_handler(sig, frame):
    print("[main] Caught Ctrl+C. Stopping")
    stopped = True
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
print("[main] Starting loop")
asyncio.run(main())
