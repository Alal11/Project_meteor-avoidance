import pygame
import random

# === 게임 설정 ===
class GameConfig:
    """게임 설정값"""
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    FPS = 60
    
    # 플레이어 설정
    PLAYER_SPEED = 4
    PLAYER_SIZE = (20, 30)
    
    # 유성 설정
    STAR_SPEED = 2
    STAR_SIZE = (20, 20)
    STAR_COUNT = 20
    STAR_SPAWN_DELAY = 5
    
    # 색상
    BACKGROUND_COLOR = (10, 10, 40)
    TEXT_COLOR = (255, 255, 255)
    GAME_OVER_COLOR = (255, 100, 100)
    RESTART_COLOR = (255, 255, 100)
    BEST_COLOR = (100, 255, 100)

class Player:
    """플레이어 클래스"""
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, GameConfig.PLAYER_SIZE)
        self.image.fill((255, 255, 255), special_flags=pygame.BLEND_MULT)
        self.rect = self.image.get_rect()
        self.reset_position()
        self.move_x = 0
        self.move_y = 0
    
    def reset_position(self):
        """플레이어 위치 초기화"""
        self.rect.centerx = GameConfig.SCREEN_WIDTH // 2
        self.rect.centery = GameConfig.SCREEN_HEIGHT // 2
    
    def handle_input(self):
        """키보드 입력 처리"""
        self.move_x = 0
        self.move_y = 0
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_x = -GameConfig.PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.move_x = GameConfig.PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.move_y = -GameConfig.PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.move_y = GameConfig.PLAYER_SPEED
    
    def update(self):
        """플레이어 위치 업데이트"""
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        
        # 경계 제한
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > GameConfig.SCREEN_WIDTH - self.rect.width:
            self.rect.x = GameConfig.SCREEN_WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > GameConfig.SCREEN_HEIGHT - self.rect.height:
            self.rect.y = GameConfig.SCREEN_HEIGHT - self.rect.height
    
    def draw(self):
        """플레이어 그리기"""
        self.screen.blit(self.image, self.rect)

class Star:
    """개별 유성 클래스"""
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('star.png')
        self.image = pygame.transform.scale(self.image, GameConfig.STAR_SIZE)
        self.rect = self.image.get_rect()
        self.active = False
        self.reset()
    
    def reset(self):
        """유성 위치 초기화"""
        self.rect.x = random.randint(0, GameConfig.SCREEN_WIDTH - GameConfig.STAR_SIZE[0])
        self.rect.y = -GameConfig.STAR_SIZE[1]
        self.active = False
    
    def activate(self):
        """유성 활성화"""
        self.rect.x = random.randint(0, GameConfig.SCREEN_WIDTH - GameConfig.STAR_SIZE[0])
        self.rect.y = 0
        self.active = True
    
    def update(self):
        """유성 이동"""
        if self.active:
            self.rect.y += GameConfig.STAR_SPEED
            if self.rect.y > GameConfig.SCREEN_HEIGHT:
                self.active = False
    
    def draw(self):
        """유성 그리기"""
        if self.active:
            self.screen.blit(self.image, self.rect)

class StarManager:
    """유성 관리 클래스"""
    def __init__(self, screen):
        self.screen = screen
        self.stars = [Star(screen) for _ in range(GameConfig.STAR_COUNT)]
        self.spawn_timer = 0
    
    def update(self):
        """모든 유성 업데이트"""
        # 유성 생성
        self.spawn_timer += 1
        if self.spawn_timer > GameConfig.STAR_SPAWN_DELAY:
            self.spawn_timer = 0
            self._spawn_star()
        
        # 모든 유성 업데이트
        for star in self.stars:
            star.update()
    
    def _spawn_star(self):
        """새 유성 생성"""
        for star in self.stars:
            if not star.active:
                star.activate()
                break
    
    def draw(self):
        """모든 유성 그리기"""
        for star in self.stars:
            star.draw()
    
    def reset(self):
        """모든 유성 초기화"""
        for star in self.stars:
            star.active = False
        self.spawn_timer = 0
    
    def get_active_stars(self):
        """활성화된 유성들 반환"""
        return [star for star in self.stars if star.active]

class ScoreManager:
    """점수 관리 클래스"""
    def __init__(self):
        self.score = 0
        self.best_score = 0
    
    def update(self):
        """점수 증가"""
        self.score += 1
    
    def reset(self):
        """점수 초기화 (최고점수 업데이트)"""
        if self.score > self.best_score:
            self.best_score = self.score
        self.score = 0

class UI:
    """UI 관리 클래스"""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 28)
    
    def draw_score(self, score):
        """점수 표시"""
        score_surface = self.font.render(f'Score: {score}', True, GameConfig.TEXT_COLOR)
        self.screen.blit(score_surface, (10, 10))
    
    def draw_game_over(self, score, best_score):
        """게임오버 화면"""
        # 게임오버 텍스트
        game_over_surface = self.big_font.render('GAME OVER', True, GameConfig.GAME_OVER_COLOR)
        game_over_rect = game_over_surface.get_rect(center=(GameConfig.SCREEN_WIDTH//2, GameConfig.SCREEN_HEIGHT//2 - 30))
        self.screen.blit(game_over_surface, game_over_rect)
        
        # 재시작 안내
        restart_surface = self.small_font.render('Press R to Restart', True, GameConfig.RESTART_COLOR)
        restart_rect = restart_surface.get_rect(center=(GameConfig.SCREEN_WIDTH//2, GameConfig.SCREEN_HEIGHT//2 + 20))
        self.screen.blit(restart_surface, restart_rect)
        
        # 최고 점수
        best_surface = self.small_font.render(f'Best: {best_score}', True, GameConfig.BEST_COLOR)
        best_rect = best_surface.get_rect(center=(GameConfig.SCREEN_WIDTH//2, GameConfig.SCREEN_HEIGHT//2 + 50))
        self.screen.blit(best_surface, best_rect)

class Game:
    """메인 게임 클래스"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Meteor Avoidance Game v3.0")
        self.clock = pygame.time.Clock()
        
        # 게임 객체들 생성
        self.player = Player(self.screen)
        self.star_manager = StarManager(self.screen)
        self.score_manager = ScoreManager()
        self.ui = UI(self.screen)
        
        # 게임 상태
        self.running = True
        self.game_over = False
        
        print("=== Meteor Avoidance Game v3.0 시작! ===")
        print("조작법: 방향키로 이동, R키로 재시작, ESC로 종료")
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r and self.game_over:
                    self.restart()
    
    def update(self):
        """게임 로직 업데이트"""
        if not self.game_over:
            # 플레이어 입력 및 이동
            self.player.handle_input()
            self.player.update()
            
            # 유성 관리
            self.star_manager.update()
            
            # 충돌 검사
            self.check_collision()
            
            # 점수 증가
            self.score_manager.update()
    
    def check_collision(self):
        """충돌 검사"""
        for star in self.star_manager.get_active_stars():
            if self.player.rect.colliderect(star.rect):
                print('게임 오버! 충돌 발생')
                self.game_over = True
                return
    
    def draw(self):
        """화면 그리기"""
        # 배경
        self.screen.fill(GameConfig.BACKGROUND_COLOR)
        
        # 게임 객체들
        self.player.draw()
        self.star_manager.draw()
        
        # UI
        self.ui.draw_score(self.score_manager.score)
        if self.game_over:
            self.ui.draw_game_over(self.score_manager.score, self.score_manager.best_score)
        
        pygame.display.flip()
    
    def restart(self):
        """게임 재시작"""
        self.score_manager.reset()
        self.player.reset_position()
        self.star_manager.reset()
        self.game_over = False
        print('게임 재시작!')
    
    def run(self):
        """메인 게임 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(GameConfig.FPS)
        
        pygame.quit()
        print("게임 종료!")

# === 게임 실행 ===
if __name__ == "__main__":
    game = Game()
    game.run()