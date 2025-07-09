class Shop:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory

    def buy(self, item, player):
        if item in self.inventory and player.cash >= item.price:
            player.cash -= item.price
            player.inventory.append(item)
            self.inventory.remove(item)
            return True
        return False

    def sell(self, item, player):
        if item in player.inventory:
            player.cash += item.price
            player.inventory.remove(item)
            self.inventory.append(item)
            return True
        return False
