import pygame

from stackframe import StackFrame, runStack

# class MenuItem(pygame.font.Font):

class Menu(StackFrame):
        
    def __init__(self, stack, window, items, position=None, background=None, color=None, highlighting=None):
        super(Menu, self).__init__(stack, window)
        if position is None:
            self.position = pygame.Rect((0, 0), (window.get_width(), window.get_height()))
        else:
            self.position = position

        self.surface = pygame.Surface((self.position.width, self.position.height))
        self.items = items
        
        if background is not None:
            self.background = pygame.image.load(background)
        if color is not None:
            self.color = color
        if highlighting is not None:
            self.highlighting = highlighting
        
    def poll(self):
        super(Menu, self).poll()
    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                xPos = event.pos[0]
                yPos = event.pos[1]
                for box in self.boxes:
                    if xPos > box[0].left and xPos < box[0].right and yPos > box[0].top and yPos < box[0].bottom:
                        if isinstance(box[1], StackFrame):
                            self.stack.append(box[1])
                        elif box[1] is None:
                            self.kill()
                        else:
                            box[1]()

    def update(self):
        super(Menu, self).update()
    
    def render(self):
        super(Menu, self).render()
    
        fontSize = 36
        fontSpace = 4
        # use the default font
        font = pygame.font.Font(None, fontSize)
        
        subHeight = (fontSize + fontSpace) * len(self.items)
        subHeightStart = self.surface.get_height() / 2 - subHeight / 2
        
        if hasattr(self, 'color'):
            self.surface.fill(self.color)
            
        if hasattr(self, 'background'):
            self.surface = self.background
        
        self.boxes = []
        
        if hasattr(self, 'background'):
            self.surface.blit(self.background, (0, 0))
        
        for item in self.items:
            text = font.render(item[0], 1, (250, 250, 250))
            textPos = text.get_rect(centerx = self.surface.get_width() / 2, centery = subHeightStart + fontSize + fontSpace)
            if hasattr(self, 'highlighting'):
                (xPos, yPos) = pygame.mouse.get_pos()
                if xPos > textPos.left and xPos < textPos.right and yPos > textPos.top and yPos < textPos.bottom:
                    text = font.render(item[0], 1, self.highlighting)
            self.boxes.append([textPos, item[1]])
            subHeightStart = subHeightStart + fontSize + fontSpace
            self.surface.blit(text, textPos)
        
    def paint(self):
        super(Menu, self).paint()
        self.window.blit(self.surface, self.position)
        
class MenuTree(Menu):
    
    def __init__(self, stack, window, items, position=None, background=None, color=None, highlighting=None):
        for item in items:
            if type(item[1]) is type([]):
                item[1].append(["Return", None])
                item[1] = MenuTree(stack, window, item[1], position, background, color, highlighting)
        
        super(MenuTree, self).__init__(stack, window, items, position, background, color, highlighting)