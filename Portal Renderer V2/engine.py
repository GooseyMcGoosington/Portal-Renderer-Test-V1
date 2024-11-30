from settings import *
import classes, level, raster

## todo: clip segments against viewing frustum from portals and what not
## render only visible walls only within the viewing frustum

class Engine:
    def __init__(self, player, main_screen):
        self.player:classes.Player=player
        self.main_screen=main_screen
        self.traversed_sectors=[]
        self.frame_buffer=frame_buffer.copy()
        self.cs=0
        self.sn=0
    def update(self):
        in_sector = self.find_sector_from_point(self.player.position.x, self.player.position.y)
        if in_sector:
            self.player.current_sector=in_sector
            self.rasterize_sector(in_sector, None)
        self.traversed_sectors = []
        self.cs = cos[self.player.yaw]
        self.sn = sin[self.player.yaw]
    def rasterize_sector(current_sector:classes.Sector, last_sector:classes.Sector):
        if current_sector != last_sector:
            sector_h = current_sector.h
            sector_e = current_sector.e
    def draw(self):
        pygame.surfarray.blit_array(self.main_screen, self.frame_buffer)
        pygame.display.update()
        self.frame_buffer = frame_buffer.copy()

    def draw_sector(self, sector: classes.Sector, count):
        player_position = self.player.position
        pygame.draw.circle(self.main_screen, YELLOW, vec2(player_position.x, player_position.y)+OFFSET, 4, width=0)
        for segment in sector.segments:
            if segment.isPortal:
                col = (0, 0, 255/count)
            else:
                col = (255/count, 0, 0)
            pygame.draw.line(self.main_screen, col, segment.p1+OFFSET, segment.p2+OFFSET, width=1)

    def point_in_polygon(self, cx, cy, walls):
        # Cast a ray to the right and count intersections
        intersections = 0
        for wall in walls:
            p1 = wall.p1
            p2 = wall.p2
            x0, y0 = p1
            x1, y1 = p2
            # Check if the point is on an edge
            if (min(y0, y1) <= cy < max(y0, y1)) and (cx < max(x0, x1)):
                if (y1 - y0) != 0:  # Avoid division by zero
                    x_intersection = x0 + (cy - y0) * (x1 - x0) / (y1 - y0)
                    if cx < x_intersection:
                        intersections += 1
        return intersections % 2 == 1
    
    def find_sector_from_point(self, x, y):
        for sector in level.sectors:
            sector_walls = sector.segments
            is_inside_sector = self.point_in_polygon(x, y, sector_walls)
            if is_inside_sector:
                return sector
        return None