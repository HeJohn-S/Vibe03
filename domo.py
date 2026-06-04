import tkinter as tk
import random

class BreakoutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("블록깨기 게임")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # 게임 캔버스
        self.canvas = tk.Canvas(root, bg="black", width=800, height=600)
        self.canvas.pack()
        
        # 게임 상태
        self.game_running = True
        self.score = 0
        self.level = 1
        
        # 공의 속성
        self.ball_size = 10
        self.ball_x = 400
        self.ball_y = 550
        self.ball_dx = random.choice([-3, 3])
        self.ball_dy = -3
        
        # 패들의 속성
        self.paddle_width = 100
        self.paddle_height = 15
        self.paddle_x = 350
        self.paddle_y = 570
        self.paddle_speed = 7
        
        # 블록의 속성
        self.blocks = []
        self.block_width = 75
        self.block_height = 20
        self.create_blocks()
        
        # 키 입력 처리
        self.keys = {}
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        
        # 게임 루프
        self.update_game()
    
    def create_blocks(self):
        """블록 생성"""
        self.blocks = []
        rows = 3
        cols = 10
        for row in range(rows):
            for col in range(cols):
                x = col * 75 + 10
                y = row * 30 + 20
                self.blocks.append({
                    'x': x,
                    'y': y,
                    'width': self.block_width,
                    'height': self.block_height,
                    'exist': True
                })
    
    def key_press(self, event):
        """키 입력 처리"""
        self.keys[event.keysym] = True
    
    def key_release(self, event):
        """키 입력 해제"""
        self.keys[event.keysym] = False
    
    def move_paddle(self):
        """패들 이동"""
        if self.keys.get('Left', False) and self.paddle_x > 0:
            self.paddle_x -= self.paddle_speed
        if self.keys.get('Right', False) and self.paddle_x < 800 - self.paddle_width:
            self.paddle_x += self.paddle_speed
    
    def move_ball(self):
        """공 이동"""
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # 벽 충돌
        if self.ball_x <= self.ball_size or self.ball_x >= 800 - self.ball_size:
            self.ball_dx *= -1
        if self.ball_y <= self.ball_size:
            self.ball_dy *= -1
        
        # 바닥 (게임 오버)
        if self.ball_y >= 600:
            self.game_running = False
    
    def check_collisions(self):
        """충돌 감지"""
        # 패들과의 충돌
        if (self.ball_y + self.ball_size >= self.paddle_y and
            self.ball_x >= self.paddle_x and
            self.ball_x <= self.paddle_x + self.paddle_width and
            self.ball_dy > 0):
            self.ball_dy *= -1
            self.ball_y = self.paddle_y - self.ball_size
        
        # 블록과의 충돌
        for block in self.blocks:
            if not block['exist']:
                continue
            
            if (self.ball_x > block['x'] and
                self.ball_x < block['x'] + block['width'] and
                self.ball_y > block['y'] and
                self.ball_y < block['y'] + block['height']):
                
                block['exist'] = False
                self.score += 10
                self.ball_dy *= -1
                break
    
    def draw(self):
        """화면 그리기"""
        self.canvas.delete("all")
        
        # 공 그리기
        self.canvas.create_oval(
            self.ball_x - self.ball_size,
            self.ball_y - self.ball_size,
            self.ball_x + self.ball_size,
            self.ball_y + self.ball_size,
            fill="white"
        )
        
        # 패들 그리기
        self.canvas.create_rectangle(
            self.paddle_x,
            self.paddle_y,
            self.paddle_x + self.paddle_width,
            self.paddle_y + self.paddle_height,
            fill="white"
        )
        
        # 블록 그리기
        for block in self.blocks:
            if block['exist']:
                self.canvas.create_rectangle(
                    block['x'],
                    block['y'],
                    block['x'] + block['width'],
                    block['y'] + block['height'],
                    fill="cyan",
                    outline="blue"
                )
        
        # 점수와 레벨 표시
        self.canvas.create_text(
            10, 10,
            text=f"점수: {self.score}",
            fill="white",
            anchor="nw",
            font=("Arial", 12)
        )
        
        self.canvas.create_text(
            350, 10,
            text=f"레벨: {self.level}",
            fill="white",
            anchor="nw",
            font=("Arial", 12)
        )
        
        # 게임 오버 또는 승리 메시지
        if not self.game_running:
            self.canvas.create_text(
                400, 300,
                text="게임 오버!",
                fill="red",
                font=("Arial", 36, "bold")
            )
            self.canvas.create_text(
                400, 350,
                text=f"최종 점수: {self.score}",
                fill="white",
                font=("Arial", 20)
            )
        
        # 모든 블록이 깨진 경우
        if all(not block['exist'] for block in self.blocks):
            self.canvas.create_text(
                400, 300,
                text="축하합니다!",
                fill="yellow",
                font=("Arial", 36, "bold")
            )
            self.canvas.create_text(
                400, 350,
                text=f"레벨 {self.level} 클리어! 점수: {self.score}",
                fill="white",
                font=("Arial", 20)
            )
            self.game_running = False
    
    def update_game(self):
        """게임 업데이트"""
        if self.game_running:
            self.move_paddle()
            self.move_ball()
            self.check_collisions()
        
        self.draw()
        self.root.after(30, self.update_game)

# 게임 실행
if __name__ == "__main__":
    root = tk.Tk()
    game = BreakoutGame(root)
    root.mainloop()
