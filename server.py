import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Yun",  # TODO: Your Battlesnake Username
            "color": "#F4C2C2",  # TODO: Personalize
            "head": "shac-caffeine",  # TODO: Personalize
            "tail": "shac-coffee",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Choose a random direction to move in
        possible_moves = ["up", "right", "down", "left"]

        head = data["you"]["body"][0]
        body = data["you"]["body"]
        health = data["you"]["health"]
        board = data["board"]
        snakes = data["board"]["snakes"]
        foods = data["board"]["food"]
        nearest_food = findNearestFood(head, foods)
        direction = getDirectionIndex(body)
        snake_heads = getSnakeHeads(body, snakes)
        

        for it in range(100):
          move = random.choice(possible_moves)
        # for move in possible_moves:
          coord = moveAsCoord(move, head)

          if len(foods) >= 1:
            if data["turn"] <= 30 or health <= 30:
              if isValidMove(board, coord, snakes) and isTowardsFood(head, coord, nearest_food):
                break
          else:
            if isValidMove(board, coord, snakes) and isAwayFromHeads(head, coord, snake_heads):
              break

          # if len(foods) >= 1 and (health <= 20 or data["turn"] <= 50):
          #   if isTowardsFood(head, coord, nearest_food) and isValidMove(board, coord, snakes):
          #     break
          if isValidMove(board, coord, snakes):
            break

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"

def isValidMove(board, coord, snakes):
  if isSnake(coord, snakes) or isOffBoard(board, coord):
    return False
  else:
    return True

def isOffBoard(board, coord):
  if coord["x"] < 0: return True
  if coord["y"] < 0: return True
  if coord["x"] >= board["width"]: return True
  if coord["y"] >= board["height"]: return True
  return False

def isSnake(coord, snakes):
  for snake in snakes:
    if coord in snake["body"]:
      return True
  return False

def moveAsCoord(move, head):
  if move == "up":
    return {"x": head["x"], "y": head["y"] + 1}
  elif move == "down":
    return {"x": head["x"], "y": head["y"] - 1}
  elif move == "right":
    return {"x": head["x"] + 1, "y": head["y"]}
  elif move == "left":
    return {"x": head["x"] - 1, "y": head["y"]}

# def goForNearestFood(head, nearest_food):
#   if nearest_food["x"] < head["x"]:
#     return "left"
#   elif nearest_food["x"] > head["x"]:
#     return "right"
#   else:
#     if nearest_food["y"] > head["y"]:
#       return "up"
#     else:
#       return "down"
  
def isTowardsFood(head, coord, food):
  if abs(food["x"] - head["x"]) >= abs(food["x"] - coord["x"]) and abs(food["y"] - head["y"]) >= abs(food["y"] - coord["y"]):
    return True
  else:
    return False

def findNearestFood(head, foods):
  nearest_food = foods[0]
  nearest_distance = calculateDistance(head, nearest_food)
  for food in foods:
    distance = calculateDistance(head, food)
    if distance < nearest_distance:
      nearest_food = food
      neareste_distance = distance
  return nearest_food

def calculateDistance(A, B):
  x_diff = A["x"] - B["x"]
  y_diff = A["y"] - B["y"]
  return abs(x_diff) + abs(y_diff)

def getDirectionIndex(body):
  if body[0]["y"] > body[1]["y"]:
    return 0
  if body[0]["x"] > body[1]["x"]:
    return 1
  if body[0]["y"] < body[1]["y"]:
    return 2
  if body[0]["x"] < body[1]["x"]:
    return 3

def getSnakeHeads(body, snakes):
  heads = []
  for snake in snakes:
    if snake["body"][0] != body[0] and len(snake["body"]) >= len(body):
      dangerous_head = snake["body"][0]
      heads.append({"x": dangerous_head["x"], "y": dangerous_head["y"]})
      heads.append({"x": dangerous_head["x"]-1, "y": dangerous_head["y"]})
      heads.append({"x": dangerous_head["x"]+1, "y": dangerous_head["y"]})
      heads.append({"x": dangerous_head["x"], "y": dangerous_head["y"]-1})
      heads.append({"x": dangerous_head["x"], "y": dangerous_head["y"]+1})
  return heads

def isAwayFromHeads(coord, snake_heads):
  if coord in snake_heads:
    return False
  return True

if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
