import random
import arcade


class Juego(arcade.Window):

    # Constructor
    def __init__(self):
        super().__init__(800, 800, "Nombre del videojuego")

        self.suelo_paredes = None
        self.cosas = None
        self.obstaculos = None

    def setup(self):
        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/entrada.tmx")
        self.suelo_paredes = arcade.tilemap.process_layer(my_map, "suelo y paredes", 1)
        self.cosas = arcade.tilemap.process_layer(my_map, "cosas", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)

    def on_draw(self):
        # Renderiza
        arcade.start_render()
        self.suelo_paredes.draw()
        self.cosas.draw()
        self.obstaculos.draw()

def main():

    # Metodo main
    window = Juego()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
