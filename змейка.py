from tkinter import *
game_width = 500
game_height = 500
snake_item = 10
snake_color1= "red"
snake_color2= "yellow"
snake_x= 24
snake_y= 24
snake_x_nav = 0
snake_y_nav = 0

tk = Tk()
tk.title ("Игра змейка на Python")
tk.resizable (0,0)
tk.wm_attributes ("-topmost", 1)
canvas=Canvas(tk, width=game_width,height=game_height, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

def snake_paint_item(canvas, x,y):
    canvas.create_rectangle(x*snake_item,y*snake_item,x*snake_item+snake_item, y*snake_item+snake_item,fill=snake_color2)
    canvas.create_rectangle(x*snake_item+2,y*snake_item+2,x*snake_item+snake_item-2, y*snake_item+snake_item-2,fill=snake_color2)
     
snake_paint_item(canvas, snake_x, snake_y)

def snake_move(event):
    global snake_x
    global snake_y
    if event.keysym == "Up":
        snake_x_nav = 0
        snake_y_nav = -1
    elif event.keysym == "Down":
        snake_x_nav = 0
        snake_y_nav = 1
    elif event.keysym == "Left":
        snake_x_nav = -1
        snake_y_nav = 0
    elif event.keysym == "Right":
        snake_x_nav = 1
        snake_y_nav = 0 
        
snake_x=snake_x+snake_x_nav
snake_y=snake_y+snake_y_nav
snake_paint_item(canvas, 10, 10)

canvas.bind_all("<KeyPress-Left>", snake_move)
canvas.bind_all("<KeyPress-Right>", snake_move)
canvas.bind_all("<KeyPress-Up>", snake_move)              
canvas.bind_all("<KeyPress-Down>", snake_move)
