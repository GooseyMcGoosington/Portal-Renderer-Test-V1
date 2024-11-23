from settings import *
import level
import raster
import classes

screenArray = blankScreenArray.copy()
sectors_traversed = []

def lerp(t, a, b):
    return a + t * (b - a)

class Engine:
    def __init__(self, player, screen, textures):
        ## globals
        global screenArray

        screenArray=blankScreenArray.copy()
        self.screen=screen
        self.player:classes.Player=player
        self.textures=textures
    def renderWall(self, wx1, wy1, wx2, wy2, z0, z1, f, c, fillPortal, visPlane, ceiling_c, floor_c, t0, t1, wall_length, fov, yaw, wall_texture, floor_texture, ceiling_texture, floor_texture_scale, ceiling_texture_scale, ceiling_distance, floor_distance, wall_height, wall_is_sky, ceiling_is_sky, v_offset, lighting):
        cx, cy = self.player.x, self.player.y

        current_ceiling_lut = ceiling_lut.copy()
        current_floor_lut = floor_lut.copy()

        sx1, sy1 = raster.transformToScreen(f, (wx1, wy1, z0))
        sx2, sy2 = raster.transformToScreen(f, (wx2, wy2, z0))
        sy3 = raster.transformYCoordToScreen(f, (wx1, wy1, z1))
        sy4 = raster.transformYCoordToScreen(f, (wx2, wy2, z1))

        current_ceiling_lut, current_floor_lut = raster.rasterize(screenArray, sx1, sx2, sy1, sy2, sy3, sy4, c, fillPortal, portal_buffer, current_ceiling_lut, current_floor_lut, wall_texture, wy1, wy2, t0, t1, wall_length, wall_height, wall_is_sky, self.player.yaw, v_offset, lighting)
        yaw = np.radians(yaw)
        if visPlane == -1:
            raster.rasterizeVisplane(screenArray, current_ceiling_lut, floor_texture, floor_texture_scale, fov, f, yaw, cx, cy, floor_distance, False, lighting, floor_c)
            raster.rasterizeVisplane(screenArray, current_floor_lut, ceiling_texture, ceiling_texture_scale, fov, f, yaw, cx, cy, ceiling_distance, ceiling_is_sky, lighting, ceiling_c)
        elif visPlane == 1:
            raster.rasterizeVisplane(screenArray, current_ceiling_lut, floor_texture, floor_texture_scale, fov, f, yaw, cx, cy, floor_distance, False, lighting, floor_c)
        elif visPlane == 2:
            raster.rasterizeVisplane(screenArray, current_floor_lut, ceiling_texture, ceiling_texture_scale, fov, f, yaw, cx, cy, ceiling_distance, ceiling_is_sky, lighting, ceiling_c)

    def renderSector(self, sector, yaw):
        if sector in sectors_traversed:
            return
        cx, cy, cz = self.player.x, self.player.y, self.player.z
        cs, sn = cos[yaw], sin[yaw]
        if sector == None:
            print('No Reference Sector; Out of Bounds or Missing Sector?')
            return
        sector_elevation = sector.e
        sector_height = sector.h
        sector_entities = sector.entities
        ceiling_c = sector.cc
        floor_c = sector.fc

        f = self.player.FocalLength
        fov = self.player.FOV

        portal_queue = []

        cz = self.player.z+self.player.h

        floor_distance = cz-sector.e
        ceiling_distance = sector.e+sector.h-cz
        # do entity rendering first
        for entity in sector_entities:
            wx0, wy0 = raster.transformVector((entity.x-cx, entity.y-cy), cs, sn)
            if wy0 < 1:
                continue
            sprite = self.textures[entity.sprite][0]
            e=cz-entity.z-entity.h
            sx0, sy0 = raster.transformToScreen(f, (wx0, wy0, e))
            raster.rasterizeSprite(screenArray, sx0, sy0, sprite, wy0, entity.scale, f)
            
        lighting = sector.lighting

        # do wall rendering last
        for wall in sector.walls:
            wall_p1 = wall.p1
            wall_p2 = wall.p2
            c=wall.c
            rx1 = wall_p1[0]-cx
            ry1 = wall_p1[1]-cy
            rx2 = wall_p2[0]-cx
            ry2 = wall_p2[1]-cy

            def_01_is_portal = wall.def_1_portal
            def_02_is_portal = wall.def_2_portal
            def_01_portal_link = wall.def_1_link
            def_02_portal_link = wall.def_2_link

            wall_texture=wall.wall_texture
            floor_texture=wall.floor_texture
            ceiling_texture=wall.ceiling_texture
            floor_texture_scale=wall.floor_texture_scale
            ceiling_texture_scale=wall.ceiling_texture_scale

            wall_length = wall.length
            wall_height = sector_height+sector_elevation
            t0, t1 = 0, 1

            wx1, wy1 = raster.transformVector((rx1, ry1), cs, sn)
            wx2, wy2 = raster.transformVector((rx2, ry2), cs, sn)

            nx1, ny1 = wx1, wy1
            nx2, ny2 = wx2, wy2

            if wy1 < 1 and wy2 < 1:
                continue
            elif wy1 < 1:
                wx1, wy1, t = raster.clip(wx1, wy1, wx2, wy2, 1, 1, W, 1)
                t1 += t/self.player.fovWidthAtY**0.5
            elif wy2 < 1:
                wx2, wy2, t = raster.clip(wx2, wy2, wx1, wy1, 1, 1, W, 1)
                t0 -= t/self.player.fovWidthAtY**0.5

            ## figure out what side we're at relative to the segment
            wall_normal_x = wall_p2[1]-wall_p1[1]
            wall_normal_y = -(wall_p2[0]-wall_p1[0])
            side = (wall_normal_x * rx1) + (wall_normal_y * ry1)
            side = side > 0 and 1 or side < 0 and -1 or 0
            # 1 = Right, -1 = Left, 0 = Colinear
            # we find out what side is being drawn, check if we can draw a portal and change how we rasterize the wall
            portal_to_render = None

            wall_is_sky = wall_texture == 'sky'
            ceiling_is_sky = ceiling_texture == 'sky'

            wall_texture = self.textures[wall_texture][0]
            floor_texture = self.textures[floor_texture][0]
            ceiling_texture = self.textures[ceiling_texture][0]
            if side == 1:
                if def_02_is_portal:
                    portal_to_render = def_02_portal_link
            elif side == -1:
                if def_01_is_portal:
                    portal_to_render = def_01_portal_link
            if portal_to_render == None:
                z0 = cz-sector_elevation
                z1 = z0-sector_height
                self.renderWall(wx1, wy1, wx2, wy2, z0, z1, f, c, False, -1, ceiling_c, floor_c, t0, t1, wall_length, fov, yaw, wall_texture, floor_texture, ceiling_texture, floor_texture_scale, ceiling_texture_scale, ceiling_distance, floor_distance, wall_height, wall_is_sky, ceiling_is_sky, 0, lighting)
            else:
                portal_bottom = wall.portal_bottom
                portal_top = wall.portal_top
                # we have a portal, so we are going to split the sector into two first. we will also check how high and how low can the portal be?
                wall_bottom = cz-sector_elevation # this is the bottom of the sector
                wall_portion_01 = wall_bottom-portal_bottom
                wall_height = portal_bottom
                self.renderWall(wx1, wy1, wx2, wy2, wall_bottom, wall_portion_01, f, c, False, 1, ceiling_c, floor_c, t0, t1, wall_length, fov, yaw, wall_texture, floor_texture, ceiling_texture, floor_texture_scale, ceiling_texture_scale, ceiling_distance, floor_distance, wall_height, wall_is_sky, ceiling_is_sky, -40, lighting)
                wall_top = wall_bottom-sector_height # this is the top of the sector
                wall_portion_02 = wall_top+portal_top
                wall_height = wall_height+portal_top
                wall_height = portal_top
                self.renderWall(wx1, wy1, wx2, wy2, wall_portion_02, wall_top, f, c, False, 2, ceiling_c, floor_c, t0, t1, wall_length, fov, yaw, wall_texture, floor_texture, ceiling_texture, floor_texture_scale, ceiling_texture_scale, ceiling_distance, floor_distance, wall_height, wall_is_sky, ceiling_is_sky, 0, lighting)
                # we now know where we rendered the bottom of the top portion and the top of the bottom portion, now we can draw the portal
               # self.renderWall(nx1, ny1, nx2, ny2, wall_portion_01, wall_portion_02, f, (127, 0, 255), True, 0, ceiling_c, floor_c, t0, t1, wall_length, fov, yaw, wall_texture, floor_texture, ceiling_texture, floor_texture_scale, ceiling_texture_scale, ceiling_distance, floor_distance, wall_height, wall_is_sky, ceiling_is_sky, 0, lighting)
                wall_height = sector_height+sector_elevation
                if not sector in portal_queue:
                    
                    sx1, sy1 = raster.transformToScreen(f, (nx1, ny1, wall_portion_01))
                    sx2, sy2 = raster.transformToScreen(f, (nx2, ny2, wall_portion_01))
                    sy3 = raster.transformYCoordToScreen(f, (nx1, ny1, wall_portion_02))
                    sy4 = raster.transformYCoordToScreen(f, (nx2, ny2, wall_portion_02))
                    portal_occluded = raster.is_portal_visible(screenArray, sx1, sx2, sy1, sy2, sy3, sy4)
                    if not portal_occluded:
                        portalSector = level.sectors[portal_to_render]
                        portal_queue.append(portalSector)
        sectors_traversed.append(sector)
        if len(portal_queue) > 0:
            for portalSector in portal_queue:
                self.renderSector(portalSector, yaw)

    def update(self, dt):
        ## globals
        global screenArray, portal_buffer, sectors_traversed
        sectors_traversed = []

        portal_buffer = blank_portal_buffer.copy()
        in_sector = self.find_sector_from_point(self.player.x, self.player.y)
        if in_sector != None:
            self.player.currentSector = in_sector
        self.player.vz -= 9.82
        self.player.z += self.player.vz/dt
        if self.player.z < self.player.currentSector.e:
            # they've hit the floor
            self.player.vz = 0
            if self.player.hasJumped:
                if pygame.time.get_ticks()-self.player.jumpTick >= 2/dt:
                    self.player.hasJumped = False
                    # we're on the ground and the cooldown is above 2

        elif self.player.z > self.player.currentSector.e+self.player.currentSector.h-self.player.h:
            self.player.vz = 0
            # they hit the ceiling

        self.player.z = min(max(self.player.z, self.player.currentSector.e), self.player.currentSector.e+self.player.currentSector.h-self.player.h)

        ## update all entities coordinates and put them in the correct sectors
        # when the entity moves, and has a velocity > 0, we will check if it is inside a new sector and set it to the new sector if so
        for sector in level.sectors:
            for entity in sector.entities:
                entity.update(dt, self, sector, entity)
                if entity.isTouchable:
                    entity.checkTouch(self.player.x, self.player.y, sector, entity)
        ## draw the current sector
        yaw = int(self.player.yaw)%360
        self.renderSector(self.player.currentSector, yaw)

    def draw(self):
        ## globals
        global screenArray

        pygame.surfarray.blit_array(self.screen, screenArray)
        pygame.display.update()
        screenArray = blankScreenArray.copy()
        """
        buffer = (ctypes.c_uint8 * (W * H * 3)).from_buffer(screenArray)
        ctypes.memset(ctypes.addressof(buffer), 0, len(buffer))
        """
        
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
            sector_walls = sector.walls
            is_inside_sector = self.point_in_polygon(x, y, sector_walls)
            if is_inside_sector:
                return sector
        return None