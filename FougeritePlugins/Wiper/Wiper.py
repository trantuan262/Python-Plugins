__author__ = 'DreTaX'
__version__ = '1.3.9'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import datetime
import sys
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

try:
    import os
except ImportError:
    Plugin.Log("Error", "Get the Extralibs!")
    raise ImportError("Get the Extralibs!")

"""
    Class
"""

IdsToWipe = []

EntityList = {

}


class Wiper:

    DecayTimer = None
    WipeTimer = None
    Path = None
    Cooldown = None
    Broadcast = None

    def On_PluginInit(self):
        ini = self.GetIni()
        num = ini.GetSetting("Settings", "DecayTimer")
        num2 = ini.GetSetting("Settings", "WipeCheckTimer")
        self.Path = ini.GetSetting("Settings", "UserDataPath")
        self.Cooldown = int(ini.GetSetting("Settings", "MaxDays"))
        self.Broadcast = self.bool(ini.GetSetting("Settings", "Broadcast"))
        self.DecayTimer = int(num) * 60000
        self.WipeTimer = int(num2) * 60000
        if self.bool(ini.GetSetting("Settings", "UseDecay")):
            self.Assign()
            Plugin.CreateTimer("Decay", self.DecayTimer).Start()
        if not "REMOVETHISCAPSLOCKEDWORD" in self.Path:
            if self.bool(ini.GetSetting("Settings", "UseDayLimit")):
                self.CollectIDs()
                Plugin.CreateTimer("Wipe", self.WipeTimer).Start()

    def bool(self, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            raise ValueError

    def Assign(self):
        ini = Plugin.GetIni("Health")
        EntityList['WoodFoundation'] = float(ini.GetSetting("Damage", "WoodFoundation"))
        EntityList['WoodDoorFrame'] = float(ini.GetSetting("Damage", "WoodDoorFrame"))
        EntityList['WoodPillar'] = float(ini.GetSetting("Damage", "WoodPillar"))
        EntityList['WoodWall'] = float(ini.GetSetting("Damage", "WoodWall"))
        EntityList['WoodCeiling'] = float(ini.GetSetting("Damage", "WoodCeiling"))
        EntityList['WoodWindowFrame'] = float(ini.GetSetting("Damage", "WoodWindowFrame"))
        EntityList['WoodStairs'] = float(ini.GetSetting("Damage", "WoodStairs"))
        EntityList['WoodRamp'] = float(ini.GetSetting("Damage", "WoodRamp"))
        EntityList['WoodSpikeWall'] = float(ini.GetSetting("Damage", "WoodSpikeWall"))
        EntityList['LargeWoodSpikeWall'] = float(ini.GetSetting("Damage", "LargeWoodSpikeWall"))
        EntityList['WoodBox'] = float(ini.GetSetting("Damage", "WoodBox"))
        EntityList['WoodBoxLarge'] = float(ini.GetSetting("Damage", "WoodBoxLarge"))
        EntityList['WoodGate'] = float(ini.GetSetting("Damage", "WoodGate"))
        EntityList['WoodGateway'] = float(ini.GetSetting("Damage", "WoodGateway"))
        EntityList['WoodenDoor'] = float(ini.GetSetting("Damage", "WoodenDoor"))
        EntityList['Wood_Shelter'] = float(ini.GetSetting("Damage", "Wood_Shelter"))
        EntityList['MetalWall'] = float(ini.GetSetting("Damage", "MetalWall"))
        EntityList['MetalCeiling'] = float(ini.GetSetting("Damage", "MetalCeiling"))
        EntityList['MetalDoorFrame'] = float(ini.GetSetting("Damage", "MetalDoorFrame"))
        EntityList['MetalPillar'] = float(ini.GetSetting("Damage", "MetalPillar"))
        EntityList['MetalFoundation'] = float(ini.GetSetting("Damage", "MetalFoundation"))
        EntityList['MetalStairs'] = float(ini.GetSetting("Damage", "MetalStairs"))
        EntityList['MetalRamp'] = float(ini.GetSetting("Damage", "MetalRamp"))
        EntityList['MetalWindowFrame'] = float(ini.GetSetting("Damage", "MetalWindowFrame"))
        EntityList['MetalDoor'] = float(ini.GetSetting("Damage", "MetalDoor"))
        EntityList['MetalBarsWindow'] = float(ini.GetSetting("Damage", "MetalBarsWindow"))
        EntityList['SmallStash'] = float(ini.GetSetting("Damage", "SmallStash"))
        EntityList['Campfire'] = float(ini.GetSetting("Damage", "Campfire"))
        EntityList['Furnace'] = float(ini.GetSetting("Damage", "Furnace"))
        EntityList['Workbench'] = float(ini.GetSetting("Damage", "Workbench"))
        EntityList['Barricade_Fence_Deployable'] = float(ini.GetSetting("Damage", "Barricade_Fence_Deployable"))
        EntityList['RepairBench'] = float(ini.GetSetting("Damage", "RepairBench"))
        EntityList['SleepingBagA'] = float(ini.GetSetting("Damage", "SleepingBagA"))
        EntityList['SingleBed'] = float(ini.GetSetting("Damage", "SingleBed"))

    def GetIni(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "UseDayLimit", "True")
            ini.AddSetting("Settings", "MaxDays", "14")
            ini.AddSetting("Settings", "UseDecay", "True")
            ini.AddSetting("Settings", "DecayTimer", "180")
            ini.AddSetting("Settings", "WipeCheckTimer", "30")
            ini.AddSetting("Settings", "Broadcast", "True")
            ini.AddSetting("Settings", "UserDataPath", "REMOVETHISCAPSLOCKEDWORD\\rust_server_Data\\userdata\\")
            ini.Save()
        return Plugin.GetIni("Settings")

    def WhiteList(self):
        if not Plugin.IniExists("WhiteList"):
            ini = Plugin.CreateIni("WhiteList")
            ini.Save()
        return Plugin.GetIni("WhiteList")

    def Replace(self, String):
        if String.startswith("0"):
            n = String.replace(String[0], '')
            return n
        return String

    def On_PlayerConnected(self, Player):
        id = Player.SteamID
        today = datetime.date.today()
        ini = self.GetIni()
        if ini.GetSetting("Objects", id) is None:
            ini.AddSetting("Objects", id, str(today))
            ini.Save()
        else:
            ini.SetSetting("Objects", id, str(today))
            ini.Save()

    def On_PlayerDisconnected(self, Player):
        id = Player.SteamID
        today = datetime.date.today()
        ini = self.GetIni()
        ini.SetSetting("Objects", id, str(today))
        ini.Save()

    def CollectIDs(self):
        pathtodir = path + self.Path
        if not os.path.exists(pathtodir):
            Plugin.Log("Error", "Path set in the INI doesn't exist.")
            return
        idlist = os.listdir(pathtodir)
        ini = self.GetIni()
        today = datetime.date.today()
        for id in idlist:
            if not ini.ContainsSetting("Objects", id):
                if long(id) == 0:
                    continue
                ini.AddSetting("Objects", id, str(today))
        ini.Save()


    def LaunchCheck(self):
        ini = self.GetIni()
        wl = self.WhiteList()
        enum = ini.EnumSection("Objects")
        today = datetime.date.today()
        for id in enum:
            if wl.GetSetting("WhiteList", id):
                continue
            v = str(ini.GetSetting("Objects", id)).split('-')
            lastseen = datetime.date(int(v[0]), int(self.Replace(v[1])), int(self.Replace(v[02])))
            count = str(today - lastseen).split(' ')
            if "00:00" in count[0]:
                continue
            count2 = int(count[0])
            if count2 > self.Cooldown:
                IdsToWipe.append(long(id))
        mc = 0
        if len(IdsToWipe) == 0:
            return mc
        for x in IdsToWipe:
            pathtodir = path + self.Path + str(x)
            if os.path.exists(pathtodir):
                idlist = os.listdir(pathtodir)
                for file in idlist:
                    os.remove(path + self.Path + str(x) + "\\" + file)
                os.rmdir(path + self.Path + str(x))
            ini.DeleteSetting("Objects", str(x))
        ini.Save()
        for ent in World.Entities:
            if long(ent.OwnerID) in IdsToWipe:
                ent.Destroy()
                mc += 1
        Plugin.Log("WipedIds", "Total Objects: " + str(mc))
        Plugin.Log("Log", "Wiped Objects: " + str(mc))
        if self.Broadcast:
            Server.BroadcastFrom("Wiper", "Wiped " + str(mc) + " unused objects!")
        del IdsToWipe[:]
        return mc

    def ForceDecay(self):
        for Entity in World.Entities:
            v = EntityList.get(Entity.Name, None)
            if v is None:
                continue
            Entity.Health -= v
            if Entity.Health <= 0:
                Entity.Destroy()

    def WipeByID(self, id):
        c = 0
        id2 = long(id)
        for ent in World.Entities:
            if long(ent.OwnerID) == id2:
                ent.Destroy()
                c += 1
        return c

    def WipeByIDList(self, list):
        c = 0
        for ent in World.Entities:
            if ent.OwnerID in list:
                ent.Destroy()
                c += 1
        return c

    def WipeCallback(self, timer):
        timer.Kill()
        if self.Broadcast:
            Server.BroadcastFrom("Wiper", "Checking for Wipeable unused objects....")
        Loom.QueueOnMainThread(lambda:
            self.LaunchCheck()
        )
        Plugin.CreateTimer("Wipe", self.WipeTimer).Start()

    def DecayCallback(self, timer):
        timer.Kill()
        self.ForceDecay()
        Plugin.CreateTimer("Decay", self.DecayTimer).Start()

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "wipehelp":
            if Player.Admin or Player.Moderator:
                Player.MessageFrom("Wiper", "Wiper Commands:")
                Player.MessageFrom("Wiper", "/wipecheck - Checks for inactive objects")
                Player.MessageFrom("Wiper", "/wipetimerreset - Restarts the timer.")
                Player.MessageFrom("Wiper", "/wipeid playerid - Wipes All the objects of the ID")
                Player.MessageFrom("Wiper", "/wipebarr - Deletes all barricaes")
                Player.MessageFrom("Wiper", "/wipecampf - Deletes all camp fires")
                Player.MessageFrom("Wiper", "/wipeforced - Force a decay")
        elif cmd == "wipecheck":
            if Player.Admin or Player.Moderator:
                if self.Broadcast:
                    Server.BroadcastFrom("Wiper", "Checking for Wipeable unused objects....")
                n = self.LaunchCheck()
                if self.Broadcast:
                    Server.BroadcastFrom("Wiper", "Wiped: " + str(n) + " objects.")
                else:
                    Player.MessageFrom("Wiper", "Wiped: " + str(n) + " objects.")
        elif cmd == "wipetimerreset":
            if Player.Admin or Player.Moderator:
                Plugin.KillTimer("Wipe")
                Plugin.KillTimer("Decay")
                Plugin.CreateTimer("Wipe", self.WipeTimer).Start()
                Plugin.CreateTimer("Decay", self.DecayTimer).Start()
                Player.MessageFrom("Wiper", "Timer restarted.")
        elif cmd == "wipeid":
            if len(args) == 0 or len(args) > 1:
                Player.MessageFrom("Wiper", "Usage: /wipeid playerid")
                return
            if not args[0].isdigit():
                Player.MessageFrom("Wiper", "The id is only made of numbers")
                return
            if Player.Admin or Player.Moderator:
                num = self.WipeByID(args[0])
                Plugin.Log("Log", Player.Name + " wiped " + args[0] + "'s objects. Total: " + str(num))
                Player.MessageFrom("Wiper", "Wiped " + str(num) + " objects!")
        elif cmd == "wipebarr":
            if Player.Admin or Player.Moderator:
                c = 0
                for ent in World.Entities:
                    if "barricade" in ent.Name.lower():
                        ent.Destroy()
                        c += 1
                Player.MessageFrom("Wiper", "Wiped " + str(c) + " barricades.")
        elif cmd == "wipecampf":
            if Player.Admin or Player.Moderator:
                c = 0
                for ent in World.Entities:
                    if "camp" in ent.Name.lower():
                        ent.Destroy()
                        c += 1
                Player.MessageFrom("Wiper", "Wiped " + str(c) + " camp fires.")
        elif cmd == "wipeforced":
            if Player.Admin or Player.Moderator:
                Player.MessageFrom("Wiper", "Forcing Decay...")
                self.ForceDecay()
                Player.MessageFrom("Wiper", "Force Decay Finished.")
        elif cmd == "wipewl":
            if Player.Admin or Player.Moderator:
                if len(args) == 0 or len(args) > 1:
                    Player.MessageFrom("Wiper", "Usage: /wipewl playerid")
                    return
                if not args[0].isdigit():
                    Player.MessageFrom("Wiper", "The id is only made of numbers")
                    return
                ini = self.WhiteList()
                if ini.GetSetting("WhiteList", args[0]) is not None:
                    Player.MessageFrom("Wiper", "Already exists!")
                    return
                ini.AddSetting("WhiteList", args[0], "1")
                ini.Save()
                Player.MessageFrom("Wiper", "Added!")
        elif cmd == "wipeall":
            if Player.Admin:
                wl = self.WhiteList()
                enum = wl.EnumSection("WhiteList")
                Server.Broadcast("Wiping objects.....")
                Store = []
                for id in enum:
                    Store.append(id)
                for e in World.Entities:
                    x = e.OwnerID
                    if x not in Store:
                        e.Destroy()
                        pathtodir = path + self.Path + str(x)
                        if os.path.exists(pathtodir):
                            idlist = os.listdir(pathtodir)
                            for file in idlist:
                                os.remove(path + self.Path + str(x) + "\\" + file)
                            os.rmdir(path + self.Path + str(x))
