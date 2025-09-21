import pygame
import random
import math

# === 게임 설정 ===
class GameConfig:
    """게임 설정값들을 한 곳에 모음"""
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    FPS = 60
    
    # 플레이어 설정
    PLAYER_SPEED = 4
    PLAYER_SIZE = (20, 30)
    
    # 유성 설정
    STAR_SIZE = (20, 20)
    STAR_COUNT = 20
    
    # 레벨 시스템
    LEVEL_UP_SCORE = 500  # 500점마다 레벨업
    MAX_LEVEL = 10
    
    # 깜빡임 설정 (레벨 5부터 시작)
    BLINK_START_LEVEL = 5
    BLINK_CYCLE = 120  # 2초 주기 (60fps 기준)
    BLINK_VISIBLE_RATIO = 0.7  # 70% 시간은 보이고 30% 시간은 안 보임
    
    # 색상
    BACKGROUND_COLOR = (10, 10, 40)
    TEXT_COLOR = (255, 255, 255)
    GAME_OVER_COLOR = (255, 100, 100)
    RESTART_COLOR = (255, 255, 100)
    BEST_COLOR = (100, 255, 100)
    LEVEL_COLOR = (100, 200, 255)

class LevelManager:
    """레벨 시스템 관리"""
    def __init__(self):
        self.level = 1
        self.score_for_next_level = GameConfig.LEVEL_UP_SCORE
    
    def update(self, score):
        """점수에 따른 레벨 업데이트"""
        new_level = min(score // GameConfig.LEVEL_UP_SCORE + 1, GameConfig.MAX_LEVEL)
        if new_level > self.level:
            self.level = new_level
            print(f"레벨 업! 현재 레벨: {self.level}")
        return self.level
    
    def get_star_speed(self):
        """레벨에 따른 유성 속도"""
        return 2 + (self.level - 1) * 0.5
    
    def get_spawn_delay(self):
        """레벨에 따른 유성 생성 딜레이"""
        return max(3, 8 - self.level)
    
    def reset(self):
        """레벨 초기화"""
        self.level = 1

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
    """개별 유성 클래스 - 깜빡임 기능 추가"""
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('star.png')
        self.image = pygame.transform.scale(self.image, GameConfig.STAR_SIZE)
        self.rect = self.image.get_rect()
        self.active = False
        self.blink_timer = 0
        self.speed = 2
        self.reset()
    
    def reset(self):
        """유성 위치 초기화"""
        self.rect.x = random.randint(0, GameConfig.SCREEN_WIDTH - GameConfig.STAR_SIZE[0])
        self.rect.y = -GameConfig.STAR_SIZE[1]
        self.active = False
        self.blink_timer = random.randint(0, GameConfig.BLINK_CYCLE)  # 랜덤 시작점
    
    def activate(self, speed):
        """유성 활성화"""
        self.rect.x = random.randint(0, GameConfig.SCREEN_WIDTH - GameConfig.STAR_SIZE[0])
        self.rect.y = 0
        self.active = True
        self.speed = speed
    
    def update(self, level):
        """유성 이동 및 깜빡임 업데이트"""
        if self.active:
            # 이동
            self.rect.y += self.speed
            if self.rect.y > GameConfig.SCREEN_HEIGHT:
                self.active = False
            
            # 깜빡임 타이머 (레벨 5부터)
            if level >= GameConfig.BLINK_START_LEVEL:
                self.blink_timer += 1
                if self.blink_timer >= GameConfig.BLINK_CYCLE:
                    self.blink_timer = 0
    
    def is_visible(self, level):
        """현재 깜빡임 상태에서 보이는지 확인"""
        if level < GameConfig.BLINK_START_LEVEL:
            return True
        
        # 깜빡임 주기 계산
        cycle_position = self.blink_timer / GameConfig.BLINK_CYCLE
        return cycle_position < GameConfig.BLINK_VISIBLE_RATIO
    
    def can_collide(self, level):
        """충돌 가능한지 확인 (보일 때만 충돌)"""
        return self.active and self.is_visible(level)
    
    def draw(self, level):
        """유성 그리기 - 깜빡임 효과"""
        if self.active and self.is_visible(level):
            # 깜빡임 레벨에서는 약간 투명하게
            if level >= GameConfig.BLINK_START_LEVEL:
                # 사인파를 이용한 부드러운 깜빡임
                alpha_factor = 0.7 + 0.3 * math.sin(self.blink_timer * 0.1)
                alpha_surface = self.image.copy()
                alpha_surface.set_alpha(int(255 * alpha_factor))
                self.screen.blit(alpha_surface, self.rect)
            else:
                self.screen.blit(self.image, self.rect)

class StarManager:
    """유성 관리 클래스"""
    def __init__(self, screen):
        self.screen = screen
        self.stars = [Star(screen) for _ in range(GameConfig.STAR_COUNT)]
        self.spawn_timer = 0
    
    def update(self, level_manager):
        """모든 유성 업데이트"""
        # 유성 생성
        self.spawn_timer += 1
        spawn_delay = level_manager.get_spawn_delay()
        if self.spawn_timer > spawn_delay:
            self.spawn_timer = 0
            self._spawn_star(level_manager.get_star_speed())
        
        # 모든 유성 업데이트
        for star in self.stars:
            star.update(level_manager.level)
    
    def _spawn_star(self, speed):
        """새 유성 생성"""
        for star in self.stars:
            if not star.active:
                star.activate(speed)
                break
    
    def draw(self, level):
        """모든 유성 그리기"""
        for star in self.stars:
            star.draw(level)
    
    def reset(self):
        """모든 유성 초기화"""
        for star in self.stars:
            star.active = False
        self.spawn_timer = 0
    
    def get_collidable_stars(self, level):
        """충돌 가능한 유성들 반환"""
        return [star for star in self.stars if star.can_collide(level)]

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
    
    def draw_game_info(self, score, level):
        """점수 및 레벨 표시"""
        # 점수
        score_surface = self.font.render(f'Score: {score}', True, GameConfig.TEXT_COLOR)
        self.screen.blit(score_surface, (10, 10))
        
        # 레벨
        level_surface = self.font.render(f'Level: {level}', True, GameConfig.LEVEL_COLOR)
        self.screen.blit(level_surface, (10, 45))
        
        # 깜빡임 안내 (레벨 5부터)
        if level >= GameConfig.BLINK_START_LEVEL:
            blink_info = self.small_font.render('Stars blink - avoid when invisible!', True, (255, 255, 100))
            self.screen.blit(blink_info, (10, 75))
    
    def draw_game_over(self, score, best_score, level):
        """게임오버 화면"""
        # 게임오버 텍스트
        game_over_surface = self.big_font.render('GAME OVER', True, GameConfig.GAME_OVER_COLOR)
        game_over_rect = game_over_surface.get_rect(center=(GameConfig.SCREEN_WIDTH//2, GameConfig.SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_surface, game_over_rect)
        
        # 최종 레벨
        level_surface = self.font.render(f'Reached Level: {level}', True, GameConfig.LEVEL_COLOR)
        level_rect = level_surface.get_rect(center=(GameConfig.SCREEN_WIDTH//2, GameConfig.SCREEN_HEIGHT//2 - 10))
        self.screen.blit(level_surface, level_rect)
        
        # 재시작 안내
        restart_surface = self.small_font.render('Press R to Restart', True, GameConfig.RESTART_COLOR)
        restart_rect = restart_surface.get_rect(center=(GameConfig.SCREEN_WIDTH//2, GameConfig.SCREEN_HEIGHT//2 + 25))
        self.screen.blit(restart_surface, restart_rect)
        
        # 최고 점수
        best_surface = self.small_font.render(f'Best: {best_score}', True, GameConfig.BEST_COLOR)
        best_rect = best_surface.get_rect(center=(GameConfig.SCREEN_WIDTH//2, GameConfig.SCREEN_HEIGHT//2 + 55))
        self.screen.blit(best_surface, best_rect)

class Game:
    """메인 게임 클래스"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Meteor Avoidance Game v4.0 - Level System")
        self.clock = pygame.time.Clock()
        
        # 게임 객체들 생성
        self.player = Player(self.screen)
        self.star_manager = StarManager(self.screen)
        self.score_manager = ScoreManager()
        self.level_manager = LevelManager()
        self.ui = UI(self.screen)
        
        # 게임 상태
        self.running = True
        self.game_over = False
        
        print("=== Meteor Avoidance Game v4.0 시작! ===")
        print("조작법: 방향키로 이동, R키로 재시작, ESC로 종료")
        print("특징: 레벨 시스템, 레벨 5부터 별이 깜빡임!")
    
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
            
            # 레벨 업데이트
            self.level_manager.update(self.score_manager.score)
            
            # 유성 관리
            self.star_manager.update(self.level_manager)
            
            # 충돌 검사
            self.check_collision()
            
            # 점수 증가
            self.score_manager.update()
    
    def check_collision(self):
        """충돌 검사 - 깜빡임 상태 고려"""
        for star in self.star_manager.get_collidable_stars(self.level_manager.level):
            if self.player.rect.colliderect(star.rect):
                print(f'게임 오버! 레벨 {self.level_manager.level}에서 충돌 발생')
                self.game_over = True
                return
    
    def draw(self):
        """화면 그리기"""
        # 배경
        self.screen.fill(GameConfig.BACKGROUND_COLOR)
        
        # 게임 객체들
        self.player.draw()
        self.star_manager.draw(self.level_manager.level)
        
        # UI
        self.ui.draw_game_info(self.score_manager.score, self.level_manager.level)
        if self.game_over:
            self.ui.draw_game_over(self.score_manager.score, self.score_manager.best_score, self.level_manager.level)
        
        pygame.display.flip()
    
    def restart(self):
        """게임 재시작"""
        self.score_manager.reset()
        self.level_manager.reset()
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