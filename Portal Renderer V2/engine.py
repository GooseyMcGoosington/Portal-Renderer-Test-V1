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
            self.rasterize_sector(in_sector, 1, (1, W1, 1, H1))
        print(self.traversed_sectors)
        self.traversed_sectors = []
        self.cs = cos[self.player.yaw]
        self.sn = sin[self.player.yaw]
        
    def rasterize_wall(self, x1, x2, y1, y2, z1, z2, c, clipping_bounds):
        f = self.player.f

        sx1, sy1 = raster.transformToScreen(f, (x1, y1, z1))
        sx2, sy2 = raster.transformToScreen(f, (x2, y2, z1))
        sy3 = raster.transformYToScreen(f, (x1, y1, z2))
        sy4 = raster.transformYToScreen(f, (x2, y2, z2))

        raster.rasterize_flat_wall(self.frame_buffer, sx1, sx2, sy1, sy2, sy3, sy4, c, clipping_bounds)
        return (sx1, sx2, sy1, sy2, sy3, sy4)
    
    def get_raster_wall(self, x1, x2, y1, y2, z1, z2):
        f = self.player.f
        sx1, sy1 = raster.transformToScreen(f, (x1, y1, z1))
        sx2, sy2 = raster.transformToScreen(f, (x2, y2, z1))
        sy3 = raster.transformYToScreen(f, (x1, y1, z2))
        sy4 = raster.transformYToScreen(f, (x2, y2, z2))
        return (sx1, sx2, sy1, sy2, sy3, sy4)
    
    def rasterize_sector(self, sector: classes.Sector, count: int, clipping_bounds):
        self.draw_sector(sector, count)
        portals=[]
        p_pos2D = (self.player.position.x, self.player.position.y)
        sector_h = sector.h
        sector_e = sector.e
        z1 = -sector_e-sector_h+5
        z2 = -sector_e+5
        for segment in sector.segments:
            r_p1 = (segment.p1.x-p_pos2D[0], segment.p1.y-p_pos2D[1])
            r_p2 = (segment.p2.x-p_pos2D[0], segment.p2.y-p_pos2D[1])
            wx1, wy1 = raster.transformVector(r_p1, self.cs, self.sn)
            wx2, wy2 = raster.transformVector(r_p2, self.cs, self.sn)
            if wy1 < 1:
                wx1, wy1, _ = raster.clip(wx1, wy1, wx2, wy2)
            elif wy2 < 1:
                wx2, wy2, _ = raster.clip(wx2, wy2, wx1, wy1)

            if segment.isPortal:
                if not segment.portalID in self.traversed_sectors:
                    self.traversed_sectors.append(segment.portalID)
                    linked_sector = level.sectors[segment.portalLink]
                    portals.append((linked_sector, segment))
            else:
                if wy1 >= 1 and wy2 >= 1:
                    self.rasterize_wall(wx1, wx2, wy1, wy2, z1, z2, segment.c, clipping_bounds)


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