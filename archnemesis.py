from collections import defaultdict
from itertools import chain

class ArchModOpt():
    basic_mods = [
        'Toxic',
        'Chaosweaver',
        'Frostweaver',
        'Permafrost',
        'Hasted',
        'Deadeye',
        'Bombardier',
        'Flameweaver',
        'Incendiary',
        'Arcane Buffer',
        'Echoist',
        'Stormweaver',
        'Dynamo',
        'Bonebreaker',
        'Bloodletter',
        'Steel-infused',
        'Gargantuan',
        'Berserker',
        'Sentinel',
        'Juggernaut',
        'Vampiric',
        'Overcharged',
        'Soul Conduit',
        'Opulent',
        'Malediction',
        'Consecrator',
        'Frenzied'
    ]

    recipe_mods = {
        'Corrupter': 'Bloodletter + Chaosweaver',
        'Necromancer': 'Bombardier + Overcharged',
        'Hexer': 'Chaosweaver + Echoist',
        'Mana Siphoner': 'Consecrator + Dynamo',
        'Assassin': 'Deadeye + Vampiric',
        'Heralding Minions': 'Dynamo + Arcane Buffer',
        'Mirror Image': 'Echoist + Soul Conduit',
        'Flame Strider': 'Flameweaver + Hasted',
        'Executioner': 'Frenzied + Berserker',
        'Frost Strider': 'Frostweaver + Hasted',
        'Rejuvenating': 'Gargantuan + Vampiric',
        'Magma Barrier': 'Incendiary + Bonebreaker',
        'Drought Bringer': 'Malediction + Deadeye',
        'Corpse Detonator': 'Necromancer + Incendiary',
        'Ice Prison': 'Permafrost + Sentinel',
        'Storm Strider': 'Stormweaver + Hasted',
        'Entangler': 'Toxic + Bloodletter',
        'Tukohama-touched': 'Bonebreaker + Executioner + Magma Barrier',
        'Arakaali-touched': 'Corpse Detonator + Entangler + Assassin',
        'Shakari-touched': 'Entangler + Soul Eater + Drought Bringer',
        'Empowered Elements': 'Evocationist + Steel-infused + Chaosweaver',
        'Abberath-touched': 'Flame Strider + Frenzied + Rejuvenating',
        'Evocationist': 'Flameweaver + Frostweaver + Stormweaver',
        'Effigy': 'Hexer + Malediction + Corrupter',
        'Brine King-touched': 'Ice Prison + Storm Strider + Heralding Minions',
        'Lunaris-touched': 'Invulnerable + Frost Strider + Empowering Minions',
        'Solaris-touched': 'Invulnerable + Magma Barrier + Empowering Minions',
        'Temporal Bubble': 'Juggernaut + Hexer + Arcane Buffer',
        'Empowering Minions': 'Necromancer + Executioner + Gargantuan',
        'Trickster': 'Overcharged + Assassin + Echoist',
        'Crystal-skinned': 'Permafrost + Rejuvenating + Berserker',
        'Invulnerable': 'Sentinel + Juggernaut + Consecrator',
        'Soul Eater': 'Soul Conduit + Necromancer + Gargantuan',
        'Treant Horde': 'Toxic + Sentinel + Steel-infused',
        'Innocence-touched': 'Lunaris-touched + Solaris-touched + Mirror Image + Mana Siphoner',
        'Kitava-touched': 'Tukohama-touched + Abberath-touched + Corrupter + Corpse Detonator'
    }

    def __init__(self, chase) -> None:
        self.chase = chase
        self.sanitize_recipes()
        self.grouped_by_lvl = {'0': self.basic_mods}
        self.mod_registry = defaultdict(dict)
        for mod in self.basic_mods:
            self.mod_registry[mod]['lvl'] = 0
            self.mod_registry[mod]['usage'] = []
        for mod in self.recipe_mods.keys():
            self.mod_registry[mod]['usage'] = []
            self.register_mod(mod)
        self.register_chase(self.chase)

    def sanitize_recipes(self):
        self.basic_mods = [mod.lower() for mod in self.basic_mods]
        new_recipe = {}
        for mod, comb in self.recipe_mods.items():
            comb_set = set([mod.lower() for mod in comb.split(' + ')])
            new_recipe[mod.lower()] = comb_set
        self.recipe_mods = new_recipe

        new_chase = {}
        for mod, comb in self.chase.items():
            new_chase[mod.lower()] = set([m.lower() for m in self.chase[mod]])
        self.chase = new_chase
    
    def register_mod(self, mod):
        recipe = self.recipe_mods[mod]
        levels = []
        for m in recipe:
            if 'lvl' not in self.mod_registry[m]:
                self.register_mod(m)
            levels.append(self.mod_registry[m]['lvl'])
        self.mod_registry[mod]['lvl'] = max(levels) + 1
        self.grouped_by_lvl.setdefault(str(self.mod_registry[mod]['lvl']), []).append(mod)

    def register_chase(self, chase, prev=[]):
        for plan, recipe in chase.items():
            for mod in recipe:
                usage = [plan] + prev
                self.mod_registry[mod]['usage'].append(usage)
                if self.mod_registry[mod]['lvl'] > 0:
                    self.register_chase({mod: self.recipe_mods[mod]}, usage)

    def show_usage(self, lvl=0):
        mods = self.grouped_by_lvl[str(lvl)]
        f = "{:<20} {:<5} {:<50}"
        print(f.format("mod", "count", "used for"))
        for m in mods:
            print(f.format(m, len(self.mod_registry[m]['usage']), str(self.mod_registry[m]['usage'])))
    
    def plan_mod(self, mod):
        f = "{:<20} {:<5} {:<50}"
        print(f.format("mod", "count", "used for"))
        print(f.format(mod, len(self.mod_registry[mod]['usage']), str(self.mod_registry[mod]['usage'])))

    def loot_mod(self, mod):
        f = "{:<20} {:<5} {:<50}"
        print(f.format("mod", "count", "used for"))
        print(f.format(mod, len(self.mod_registry[mod]['usage']), str([m[0] for m in self.mod_registry[mod]['usage']])))
    
    def use_mod(self, mod):
        usage = self.mod_registry[mod]['usage']
        f = "{:<15} {:<10}"
        f += "{:<15} {:<8}" * len(usage)
        header = ['usage', 'count'] * len(usage)
        details = list(chain.from_iterable((u[0], usage.count(u)) for u in usage))
        print(f.format('mod', 'total count', *header))
        print(f.format(mod, sum(details[::2]), *details))
    
    def check_mod(self, word):
        if word not in self.basic_mods:
            print(word, ": ", self.recipe_mods[word])

class CmdManager():
    def __init__(self, optimizer):
        self.opt = optimizer
        self.run = True
        self.supported_cmds = {
            'use': self.opt.use_mod,
            'plan': self.opt.plan_mod,
            'loot': self.opt.loot_mod,
            'check': self.opt.check_mod
        }
    
    def prep_input(self, i):
        for cmd in self.supported_cmds.keys():
            if i[0] in cmd:
                # taking care some mods with space in its name
                return {'mod': " ".join(i[1:]), 'exec': self.supported_cmds[cmd]}
        return None

    def match_word(self, word):
        mods = opt.basic_mods + list(opt.recipe_mods.keys())
        matches = []
        for m in mods:
            if word in m:
                matches.append(m)
        return matches
        
    def start(self):
        while self.run:
            i = input("How can I help you? (one mod at a time)\n").split()
            if 'end' in i:
                self.run = False
            else:
                ctx = self.prep_input(i)
                matched_mods = self.match_word(ctx['mod'].lower())
                for mod in matched_mods:
                    ctx['exec'](mod)


if __name__ == '__main__':
    chase_recipes = {
        'currency': set(['Innocence-touched', 'Treant Horde', 'Kitava-touched', 'Brine King-touched']),
        'unique': set(['Shakari-touched', 'Treant Horde', 'Brine King-touched', 'Kitava-touched'])
    }

    opt = ArchModOpt(chase_recipes)
    cl = CmdManager(opt)
    cl.start()



