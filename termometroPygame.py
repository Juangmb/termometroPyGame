import pygame, sys
from pygame.locals import *

class Termometro():
    def __init__(self):
        self.costume = pygame.image.load("termometro/termo1.png")
    
    def convertir(self,grados, toUnidad):
        resultado = 0
        if toUnidad == "F":
            resultado = grados * 9/5 + 32
        elif toUnidad == "C":
            resultado = (grados - 32) * 5/9
        else:
            resultado = grados
            
        return "{:10.2f}".format(resultado)

class Selector():
    __tipoUnidad = None
    
    def __init__(self, unidad="C"):
        self.__costumes = []
        self.__costumes.append(pygame.image.load("termometro/posiC.png"))
        self.__costumes.append(pygame.image.load("termometro/posiF.png"))
        
        self.__tipoUnidad = unidad
        
    def costume(self):
        if self.__tipoUnidad == "F":
            return self.__costumes[1]
        else:
            return self.__costumes[0]
    
    def change(self):
        if self.__tipoUnidad == "C":
            self.__tipoUnidad = "F"
        else:
            self.__tipoUnidad = "C"
            
    def unidad(self):
        return self.__tipoUnidad

class NumberInput():
    __valor = 0
    __strValor = ""
    __position = [0, 0]
    __size = [0, 0]
    __pointsCount = 0
    
    def __init__(self, valor=0):
        self.__font = pygame.font.SysFont("Arial", 24)
        self.value(valor)
                
    def on_event(self,event):
        if event.type == KEYDOWN:
            if event.unicode.isdigit() and len(self.__strValor) <= 10 or event.unicode == "." and self.__pointsCount == 0:
                self.__strValor += event.unicode
                self.value(self.__strValor)
                if event.unicode == ".":
                    self.__pointsCount += 1
            elif event.key == K_BACKSPACE:
                if self.__strValor[-1] == ".":
                    self.__pointsCount -= 1
                self.__strValor = self.__strValor[:-1]
                self.value(self.__strValor)
                
                    
    def render(self):
        textBlock = self.__font.render(self.__strValor, True, (74,74,74))
        rect = textBlock.get_rect()
        rect.left = self.__position[0]
        rect.top = self.__position[1]
        rect.size = self.__size
                
        return {
            "fondo":rect,
            "texto":textBlock
            }
    
    def value(self,val=None):
        if val==None:
            return self.__valor
        else:
            val = str(val)
            try:
                self.__valor = float(val)
                self.__strValor = val
                if "." in self.__strValor:
                    self.__pointsCount = 1
                else:
                    self.__pointsCount = 0
            except:
                pass
    def width(self,val=None):
        if val==None:
            return self.__size[0]
        else:
            try:
                self.__size[0] = int(val)
            except:
                pass
    
    def height(self,val=None):
        if val==None:
            return self.__size[1]
        else:
            try:
                self.__size[1] = int(val)
            except:
                pass
    
    def size(self,val=None):
        if val==None:
            return self.__size
        else:
            try:
                w = int(val[0])
                h = int(val[1])
                self.__size = [int(val[0]), int(val[1])]
            except:
                pass

    def posX(self,val=None):
        if val==None:
            return self.__position[0]
        else:
            try:
                self.__position[0] = int(val)
            except:
                pass
    
    def posY(self,val=None):
        if val==None:
            return self.__position[1]
        else:
            try:
                self.__position[1] = int(val)
            except:
                pass
    
    def pos(self,val=None):
        if val==None:
            return self.__position
        else:
            try:
                w = int(val[0])
                h = int(val[1])
                self.__position = [int(val[0]), int(val[1])]
            except:
                pass

class mainApp():
    termometro = None
    entrada = None
    selector = None
    
    def __init__(self):
        self.__screen = pygame.display.set_mode((290,415))
        pygame.display.set_caption("Termometro")
        self.__screen.fill((244,236,203))
        
        self.termometro = Termometro()
        self.entrada = NumberInput()
        self.entrada.pos((106,58))
        self.entrada.size((133,28))
        
        self.selector = Selector()
    
    def __on_close(self):
        pygame.quit()
        sys.exit()
        
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__on_close()
            
                self.entrada.on_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.selector.change()
                    grados = self.entrada.value()
                    nuevaUnidad = self.selector.unidad()
                    temperatura = self.termometro.convertir(grados, nuevaUnidad)
                    self.entrada.value(temperatura)
            
            self.__screen.fill((244,236,203))
            
            self.__screen.blit(self.termometro.costume,(50,34))
            
            text = self.entrada.render()
            pygame.draw.rect(self.__screen,(255,255,255), text["fondo"])
            self.__screen.blit(text["texto"],(110,58))
            
            self.__screen.blit(self.selector.costume(),(112,153))
            
            pygame.display.flip()
        

if __name__ == "__main__":
    pygame.init()
    app = mainApp()
    app.start()