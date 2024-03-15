class perro:
    
    def __init__(self): 
        alimento = 'croquetas'   
        pass

    def get(self):
        print("scrapeando amazon")
        print("el perro come: ",self.alimento)
        return 'perro'
    def ladrar(self,nivel):
        print("ladrando"+nivel)
        
p1=perro()
print(p1.alimento)
