from settings import *
import classes, sys, level
s = 10

class BSP_Node:
    def __init__(self):
        self.front=None
        self.back=None
        self.splitter:classes.Segment=None
        self.id=0
        self.segments=[]

class BSP:
    def __init__(self, player,screen):
        self.raw_scene=[]
        self.scene=[]
        self.player=player
        for sector in level.sectors:
            self.raw_scene.extend(sector.walls[:])
        self.root_node=BSP_Node()
        self.id=0
        self.build(self.root_node, self.raw_scene)
        self.screen=screen
    def classify_point(self, plane, point):
        plane_p1 = plane.p1
        plane_p2 = plane.p2
        plane_dx = plane_p2.x - plane_p1.x
        plane_dy = plane_p2.y - plane_p1.y   
        
        return (point.x - plane_p1.x) * plane_dy - (point.y - plane_p1.y) * plane_dx
    def partition(self, node:BSP_Node, segments):
        plane = segments[0]
        plane_p1 = plane.p1
        plane_p2 = plane.p2
        plane_dx = plane_p2.x - plane_p1.x
        plane_dy = plane_p2.y - plane_p1.y   
        
        front=[]
        back=[]
        for segment in segments[1:]:
            start_side = self.classify_point(plane, segment.p1)
            end_side = self.classify_point(plane, segment.p2)

            if start_side >= 0 and end_side >= 0:
                # Entirely in front
                front.append(segment)
            elif start_side <= 0 and end_side <= 0:
                # Entirely in back
                back.append(segment)
            else:
                # Split the segment
                intersection = self.calculate_intersection(plane_p1, plane_p2, segment.p1, segment.p2)
                if start_side > 0:
                    front.append(classes.Segment(segment.p1.x, segment.p1.y, intersection.x, intersection.y, 0, 0, 0, 0,0 ,0, 0, 0,0 ,0, 0, 0))
                    back.append(classes.Segment(intersection.x, intersection.y, segment.p2.x, segment.p2.y, 0, 0, 0, 0,0 ,0, 0, 0,0 ,0, 0, 0))
                else:
                    back.append(classes.Segment(segment.p1.x, segment.p1.y, intersection.x, intersection.y, 0, 0, 0, 0,0 ,0, 0, 0,0 ,0, 0, 0))
                    front.append(classes.Segment(intersection.x, intersection.y, segment.p2.x, segment.p2.y, 0, 0, 0, 0,0 ,0, 0, 0,0 ,0, 0, 0))

        node.splitter=plane
        return front, back
    def calculate_intersection(self, p1, p2, q1, q2):
        # Calculate the intersection point of two line segments (p1-p2 and q1-q2)
        dx1, dy1 = p2.x - p1.x, p2.y - p1.y
        dx2, dy2 = q2.x - q1.x, q2.y - q1.y

        denom = dx1 * dy2 - dy1 * dx2
        if denom == 0:
            raise ValueError("Lines are parallel and cannot intersect!")

        t = ((q1.x - p1.x) * dy2 - (q1.y - p1.y) * dx2) / denom
        intersection_x = p1.x + t * dx1
        intersection_y = p1.y + t * dy1

        return vec2(intersection_x, intersection_y)
    def build(self, node:BSP_Node, segments):
        if not segments:
            return None
        front, back = self.partition(node, segments)
        #print(f"Node ID: {node.id}, Splitter: {node.splitter}, Front: {len(front)}, Back: {len(back)}")
        if len(front) > 0:
            node.front=BSP_Node()
            node.front.id=self.id
            node.segments=front
            self.id+=1
            self.build(node.front, front)
        if len(back) > 0:
            node.back=BSP_Node()
            node.back.id=self.id
            node.segments=back
            self.id+=1
            self.build(node.back, back)
    def is_on_front(self, vec_0: vec2, vec_1: vec2):
        # whether vec_0 is on the front side relative to vec_1
        return vec_0.x * vec_1.y < vec_1.x * vec_0.y
    def traverse_node(self, node:BSP_Node):
        if node == None:
            return
        splitter = node.splitter
        splitter_dy = splitter.p2.y-splitter.p1.y
        splitter_dx = splitter.p2.x-splitter.p1.x

        playerPos = vec2(self.player.x, self.player.y)
        on_front = self.is_on_front(playerPos-splitter.p1, splitter.p1-splitter.p2)
        if on_front:
            self.traverse_node(node.front)
            self.draw_segment(node.splitter, self.screen, RED)   
            self.traverse_node(node.back)
        else:
            self.traverse_node(node.back)
            self.traverse_node(node.front)
    def draw_segment(self, segment, screen, color=(255, 255, 255)):
        # Assuming screen is a 2D rendering surface and classes.Segment has p1 and p2 attributes
        pygame.draw.line(
            screen,
            color,
            (segment.p1.x*s+W2, segment.p1.y*s+H2),
            (segment.p2.x*s+W2, segment.p2.y*s+H2),
            width=2  # Optional: thickness of the line
        )
        pygame.draw.circle(screen, PINK, (segment.p1.x*s+W2, segment.p1.y*s+H2), 3)
        pygame.draw.circle(screen, PINK, (segment.p2.x*s+W2, segment.p2.y*s+H2), 3)