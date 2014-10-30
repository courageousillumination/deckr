def Solitaire(CardGame):
    
    def set_up(self):
        cards = StandardPlayingCardDeck()
        for i  in range(0, 7):
            for j in range(0, i):
                self.play_zones[i].push(cards.pop())
            self.play_zones[i][-1].reveal_to(self.player)
        self.deck = cards
          
    def game_over(self):
        for i in range(0, 3):
            if len(self.victory_zone[i]) != 13:
                return False
        return True
    
    @action(card.revealed_to(self.player) and
            (target_zone[-1].number == card.number + 1 or
             (target_zone.empty() and card.number = 13))
    def move_card(self, card, target_zone):
        old_zone = card.zone
        card.zone.remove(card)
        card.zone = target_zone
        target_zone.add(card)
        
        if old_zone[-1].revealed_to(self.player) == False:
            old_zone[-1].reveal_to(self.player)
            
    @action(not (deck.empty() and hand.empty())
    def draw_card(self):
        if deck.empty():
            deck = hand
            hand =  []
           
        card = self.deck.pop()
        self.hand.push(card)
        card.reveal_to(self.player)
    
    