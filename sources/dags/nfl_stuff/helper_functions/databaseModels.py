from sqlalchemy import ForeignKey, Column, String, Integer, Float, DATETIME
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    player_id = Column('player_id', Integer, primary_key=True, unique=True, nullable=False)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    position = Column('position', String, nullable=False)
    first_year = Column('first_year', Integer, nullable=True, default=None)
    last_year = Column('last_year', Integer, nullable=True, default=None)

    game_stats = relationship('GameStats', back_populates='player')
    season_stats = relationship('SeasonStats', back_populates='player')
    career_stats = relationship('CareerStats', back_populates='player')
    career_avg_stats = relationship('CareerAvgStats', back_populates='player')
    season_avg_stats = relationship('SeasonAvgStats', back_populates='player')
    career_totals = relationship('CareerTotals', back_populates='player')

    def __repr__(self) -> str:
        return f"<Player(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, position={self.position}, first_year={self.first_year}, last_year={self.last_year})>"

class Game(Base):
    __tablename__ = 'games'

    game_id = Column('game_id', Integer, primary_key=True, unique=True, nullable=False)
    szn = Column('szn', Integer, nullable=False)
    date = Column('date', DATETIME, nullable=False)
    home_team = Column('home_team', String, nullable=False)
    away_team = Column('away_team', String, nullable=False)
    home_score = Column('home_score', Integer, nullable=False)
    away_score = Column('away_score', Integer, nullable=False)
    game_type = Column('game_type', String, nullable=False)

    game_stats = relationship('GameStats', back_populates='games')
    team_stats = relationship('TeamStats', back_populates='games')
    career_avg_stats = relationship('CareerAvgStats', back_populates='games')
    season_avg_stats = relationship('SeasonAvgStats', back_populates='games')
    team_avg_stats = relationship('TeamAvgStats', back_populates='games')
    career_totals = relationship('CareerTotals', back_populates='games')

    def __repr__(self) -> str:
        return f"<Game(id={self.game_id}, szn={self.szn}, date='{self.date}', home_team={self.home_team}, away_team={self.away_team}, home_score={self.home_score}, away_score={self.away_score}, game_type={self.game_type})>"
    

class GameStats(Base):
    __tablename__ = 'game_stats'

    game_id = Column('game_id', Integer, ForeignKey('games.game_id'), primary_key=True, nullable=False)
    szn = Column('szn', Integer, nullable=False)
    date = Column('date', DATETIME, nullable=False)
    player_id = Column('player_id', Integer, ForeignKey('players.player_id'), primary_key=True, nullable=False)
    team = Column('team', String, nullable=False)
    passing_cmp = Column('passing_cmp', Integer, nullable=True, default=None)
    passing_att = Column('passing_att', Integer, nullable=True, default=None)
    passing_cmp_prc = Column('passing_cmp_prc', Float, nullable=True, default=None)
    passing_yds = Column('passing_yds', Integer, nullable=True, default=None)
    passing_tds = Column('passing_tds', Integer, nullable=True, default=None)
    passing_int = Column('passing_int', Integer, nullable=True, default=None)
    passing_rate = Column('passing_rate', Float, nullable=True, default=None)
    passing_sacks = Column('passing_sacks', Integer, nullable=True, default=None)
    passing_sack_yds_lost = Column('passing_sack_yds_lost', Integer, nullable=True, default=None)
    passing_yds_att = Column('passing_yds_att', Float, nullable=True, default=None)
    passing_adj_yds_att = Column('passing_adj_yds_att', Float, nullable=True, default=None)
    rushing_att = Column('rushing_att', Integer, nullable=True, default=None)
    rushing_yds = Column('rushing_yds', Integer, nullable=True, default=None)
    rushing_yds_att = Column('rushing_yds_att', Float, nullable=True, default=None)
    rushing_tds = Column('rushing_tds', Integer, nullable=True, default=None)
    scoring_tds = Column('scoring_tds', Integer, nullable=True, default=None)
    scoring_pts = Column('scoring_pts', Integer, nullable=True, default=None)
    receiving_rec = Column('receiving_rec', Integer, nullable=True, default=None)
    receiving_yds = Column('receiving_yds', Integer, nullable=True, default=None)
    receiving_yds_rec = Column('receiving_yds_rec', Float, nullable=True, default=None)
    receiving_tds = Column('receiving_tds', Integer, nullable=True, default=None)
    receiving_tgts = Column('receiving_tgts', Integer, nullable=True, default=None)
    receiving_catch_prc = Column('receiving_catch_prc', Float, nullable=True, default=None)
    receiving_yds_tgt = Column('receiving_yds_tgt', Float, nullable=True, default=None)
    fumbles_fmb = Column('fumbles_fmb', Integer, nullable=True, default=None)
    fumbles_fl = Column('fumbles_fl', Integer, nullable=True, default=None)
    off_snap_num = Column('off_snap_num', Integer, nullable=True, default=None)
    off_snap_prc = Column('off_snap_prc', Float, nullable=True, default=None)
    st_snap_num = Column('st_snap_num', Integer, nullable=True, default=None)
    st_snap_prc = Column('st_snap_prc', Float, nullable=True, default=None)

    player = relationship('Player', back_populates='game_stats')
    games = relationship('Game', back_populates='game_stats')

class SeasonStats(Base):
    __tablename__ = 'season_stats'

    player_id = Column('player_id', Integer, ForeignKey('players.player_id'), primary_key=True, nullable=False)
    szn = Column('szn', Integer, primary_key=True, nullable=False)
    player_name = Column('player_name', String, nullable=False)
    team = Column('team', String, nullable=False)
    games_played = Column('games_played', Integer, nullable=False)
    passing_cmp = Column('passing_cmp', Integer, nullable=True, default=None)
    passing_att = Column('passing_att', Integer, nullable=True, default=None)
    passing_cmp_prc = Column('passing_cmp_prc', Float, nullable=True, default=None)
    passing_yds = Column('passing_yds', Integer, nullable=True, default=None)
    passing_tds = Column('passing_tds', Integer, nullable=True, default=None)
    passing_int = Column('passing_int', Integer, nullable=True, default=None)
    passing_rate = Column('passing_rate', Float, nullable=True, default=None)
    passing_sacks = Column('passing_sacks', Integer, nullable=True, default=None)
    passing_sack_yds_lost = Column('passing_sack_yds_lost', Integer, nullable=True, default=None)
    passing_yds_att = Column('passing_yds_att', Float, nullable=True, default=None)
    passing_adj_yds_att = Column('passing_adj_yds_att', Float, nullable=True, default=None)
    rushing_att = Column('rushing_att', Integer, nullable=True, default=None)
    rushing_yds = Column('rushing_yds', Integer, nullable=True, default=None)
    rushing_yds_att = Column('rushing_yds_att', Float, nullable=True, default=None)
    rushing_tds = Column('rushing_tds', Integer, nullable=True, default=None)
    scoring_tds = Column('scoring_tds', Integer, nullable=True, default=None)
    scoring_pts = Column('scoring_pts', Integer, nullable=True, default=None)
    receiving_rec = Column('receiving_rec', Integer, nullable=True, default=None)
    receiving_yds = Column('receiving_yds', Integer, nullable=True, default=None)
    receiving_yds_rec = Column('receiving_yds_rec', Float, nullable=True, default=None)
    receiving_tds = Column('receiving_tds', Integer, nullable=True, default=None)
    receiving_tgts = Column('receiving_tgts', Integer, nullable=True, default=None)
    receiving_catch_prc = Column('receiving_catch_prc', Float, nullable=True, default=None)
    receiving_yds_tgt = Column('receiving_yds_tgt', Float, nullable=True, default=None)
    fumbles_fmb = Column('fumbles_fmb', Integer, nullable=True, default=None)
    fumbles_fl = Column('fumbles_fl', Integer, nullable=True, default=None)   

    player = relationship('Player', back_populates='season_stats')

class CareerStats(Base):
    __tablename__ = 'career_stats'

    player_id = Column('player_id', Integer, ForeignKey('players.player_id'), primary_key=True, nullable=False)
    player_name = Column('player_name', String, nullable=False)
    games_played = Column('games_played', Integer, nullable=False)
    passing_cmp = Column('passing_cmp', Integer, nullable=True, default=None)
    passing_att = Column('passing_att', Integer, nullable=True, default=None)
    passing_cmp_prc = Column('passing_cmp_prc', Float, nullable=True, default=None)
    passing_yds = Column('passing_yds', Integer, nullable=True, default=None)
    passing_tds = Column('passing_tds', Integer, nullable=True, default=None)
    passing_int = Column('passing_int', Integer, nullable=True, default=None)
    passing_rate = Column('passing_rate', Float, nullable=True, default=None)
    passing_sacks = Column('passing_sacks', Integer, nullable=True, default=None)
    passing_sack_yds_lost = Column('passing_sack_yds_lost', Integer, nullable=True, default=None)
    passing_yds_att = Column('passing_yds_att', Float, nullable=True, default=None)
    passing_adj_yds_att = Column('passing_adj_yds_att', Float, nullable=True, default=None)
    rushing_att = Column('rushing_att', Integer, nullable=True, default=None)
    rushing_yds = Column('rushing_yds', Integer, nullable=True, default=None)
    rushing_yds_att = Column('rushing_yds_att', Float, nullable=True, default=None)
    rushing_tds = Column('rushing_tds', Integer, nullable=True, default=None)
    scoring_tds = Column('scoring_tds', Integer, nullable=True, default=None)
    scoring_pts = Column('scoring_pts', Integer, nullable=True, default=None)
    receiving_rec = Column('receiving_rec', Integer, nullable=True, default=None)
    receiving_yds = Column('receiving_yds', Integer, nullable=True, default=None)
    receiving_yds_rec = Column('receiving_yds_rec', Float, nullable=True, default=None)
    receiving_tds = Column('receiving_tds', Integer, nullable=True, default=None)
    receiving_tgts = Column('receiving_tgts', Integer, nullable=True, default=None)
    receiving_catch_prc = Column('receiving_catch_prc', Float, nullable=True, default=None)
    receiving_yds_tgt = Column('receiving_yds_tgt', Float, nullable=True, default=None)
    fumbles_fmb = Column('fumbles_fmb', Integer, nullable=True, default=None)
    fumbles_fl = Column('fumbles_fl', Integer, nullable=True, default=None)

    player = relationship('Player', back_populates='career_stats')


class TeamStats(Base):
    __tablename__ = 'team_stats'

    game_id = Column('game_id', Integer, ForeignKey('games.game_id'), primary_key=True, nullable=False)
    szn = Column('szn', Integer, nullable=False)
    date = Column('date', DATETIME, nullable=False)
    team = Column('team', String, primary_key=True, nullable=False)
    passing_cmp = Column('passing_cmp', Integer, nullable=True, default=None)
    passing_att = Column('passing_att', Integer, nullable=True, default=None)
    passing_cmp_prc = Column('passing_cmp_prc', Float, nullable=True, default=None)
    passing_yds = Column('passing_yds', Integer, nullable=True, default=None)
    passing_tds = Column('passing_tds', Integer, nullable=True, default=None)
    passing_int = Column('passing_int', Integer, nullable=True, default=None)
    passing_rate = Column('passing_rate', Float, nullable=True, default=None)
    passing_sacks = Column('passing_sacks', Integer, nullable=True, default=None)
    passing_sack_yds_lost = Column('passing_sack_yds_lost', Integer, nullable=True, default=None)
    passing_yds_att = Column('passing_yds_att', Float, nullable=True, default=None)
    passing_net_yds_att = Column('passing_net_yds_att', Float, nullable=True, default=None)
    rushing_att = Column('rushing_att', Integer, nullable=True, default=None)
    rushing_yds = Column('rushing_yds', Integer, nullable=True, default=None)
    rushing_yds_att = Column('rushing_yds_att', Float, nullable=True, default=None)
    rushing_tds = Column('rushing_tds', Integer, nullable=True, default=None)
    scoring_tds = Column('scoring_tds', Integer, nullable=True, default=None)
    scoring_pts = Column('scoring_pts', Integer, nullable=True, default=None)
    punts = Column('punts', Integer, nullable=True, default=None)
    punt_yds = Column('punt_yds', Integer, nullable=True, default=None)
    third_down_conv = Column('third_down_conv', Integer, nullable=True, default=None)
    third_down_att = Column('third_down_att', Integer, nullable=True, default=None)
    fourth_down_conv = Column('fourth_down_conv', Integer, nullable=True, default=None)
    fourth_down_att = Column('fourth_down_att', Integer, nullable=True, default=None)

    games = relationship('Game', back_populates='team_stats')




class CareerAvgStats(Base):
    __tablename__ = 'career_avg_stats'

    game_id = Column('game_id', Integer, ForeignKey('games.game_id'), primary_key=True, nullable=False)
    szn = Column('szn', Integer, nullable=False)
    date = Column('date', DATETIME, nullable=False)
    player_id = Column('player_id', Integer, ForeignKey('players.player_id'), primary_key=True, nullable=False)
    team = Column('team', String, nullable=False)
    passing_cmp = Column('passing_cmp', Float, nullable=True, default=None)
    passing_att = Column('passing_att', Float, nullable=True, default=None)
    passing_cmp_prc = Column('passing_cmp_prc', Float, nullable=True, default=None)
    passing_yds = Column('passing_yds', Float, nullable=True, default=None)
    passing_tds = Column('passing_tds', Float, nullable=True, default=None)
    passing_int = Column('passing_int', Float, nullable=True, default=None)
    passing_rate = Column('passing_rate', Float, nullable=True, default=None)
    passing_sacks = Column('passing_sacks', Float, nullable=True, default=None)
    passing_sack_yds_lost = Column('passing_sack_yds_lost', Float, nullable=True, default=None)
    passing_yds_att = Column('passing_yds_att', Float, nullable=True, default=None)
    passing_adj_yds_att = Column('passing_adj_yds_att', Float, nullable=True, default=None)
    rushing_att = Column('rushing_att', Float, nullable=True, default=None)
    rushing_yds = Column('rushing_yds', Float, nullable=True, default=None)
    rushing_yds_att = Column('rushing_yds_att', Float, nullable=True, default=None)
    rushing_tds = Column('rushing_tds', Float, nullable=True, default=None)
    scoring_tds = Column('scoring_tds', Float, nullable=True, default=None)
    scoring_pts = Column('scoring_pts', Float, nullable=True, default=None)
    receiving_rec = Column('receiving_rec', Float, nullable=True, default=None)
    receiving_yds = Column('receiving_yds', Float, nullable=True, default=None)
    receiving_yds_rec = Column('receiving_yds_rec', Float, nullable=True, default=None)
    receiving_tds = Column('receiving_tds', Float, nullable=True, default=None)
    receiving_tgts = Column('receiving_tgts', Float, nullable=True, default=None)
    receiving_catch_prc = Column('receiving_catch_prc', Float, nullable=True, default=None)
    receiving_yds_tgt = Column('receiving_yds_tgt', Float, nullable=True, default=None)
    fumbles_fmb = Column('fumbles_fmb', Float, nullable=True, default=None)
    fumbles_fl = Column('fumbles_fl', Float, nullable=True, default=None)

    player = relationship('Player', back_populates='career_avg_stats')
    games = relationship('Game', back_populates='career_avg_stats')


class SeasonAvgStats(Base):
    __tablename__ = 'season_avg_stats'

    game_id = Column('game_id', Integer, ForeignKey('games.game_id'), primary_key=True, nullable=False)
    szn = Column('szn', Integer, nullable=False)
    date = Column('date', DATETIME, nullable=False)
    player_id = Column('player_id', Integer, ForeignKey('players.player_id'), primary_key=True, nullable=False)
    team = Column('team', String, nullable=False)
    passing_cmp = Column('passing_cmp', Float, nullable=True, default=None)
    passing_att = Column('passing_att', Float, nullable=True, default=None)
    passing_cmp_prc = Column('passing_cmp_prc', Float, nullable=True, default=None)
    passing_yds = Column('passing_yds', Float, nullable=True, default=None)
    passing_tds = Column('passing_tds', Float, nullable=True, default=None)
    passing_int = Column('passing_int', Float, nullable=True, default=None)
    passing_rate = Column('passing_rate', Float, nullable=True, default=None)
    passing_sacks = Column('passing_sacks', Float, nullable=True, default=None)
    passing_sack_yds_lost = Column('passing_sack_yds_lost', Float, nullable=True, default=None)
    passing_yds_att = Column('passing_yds_att', Float, nullable=True, default=None)
    passing_adj_yds_att = Column('passing_adj_yds_att', Float, nullable=True, default=None)
    rushing_att = Column('rushing_att', Float, nullable=True, default=None)
    rushing_yds = Column('rushing_yds', Float, nullable=True, default=None)
    rushing_yds_att = Column('rushing_yds_att', Float, nullable=True, default=None)
    rushing_tds = Column('rushing_tds', Float, nullable=True, default=None)
    scoring_tds = Column('scoring_tds', Float, nullable=True, default=None)
    scoring_pts = Column('scoring_pts', Float, nullable=True, default=None)
    receiving_rec = Column('receiving_rec', Float, nullable=True, default=None)
    receiving_yds = Column('receiving_yds', Float, nullable=True, default=None)
    receiving_yds_rec = Column('receiving_yds_rec', Float, nullable=True, default=None)
    receiving_tds = Column('receiving_tds', Float, nullable=True, default=None)
    receiving_tgts = Column('receiving_tgts', Float, nullable=True, default=None)
    receiving_catch_prc = Column('receiving_catch_prc', Float, nullable=True, default=None)
    receiving_yds_tgt = Column('receiving_yds_tgt', Float, nullable=True, default=None)
    fumbles_fmb = Column('fumbles_fmb', Float, nullable=True, default=None)
    fumbles_fl = Column('fumbles_fl', Float, nullable=True, default=None)

    player = relationship('Player', back_populates='season_avg_stats')
    games = relationship('Game', back_populates='season_avg_stats')



class TeamAvgStats(Base):
    __tablename__ = 'team_avg_stats'

    game_id = Column('game_id', Integer, ForeignKey('games.game_id'), primary_key=True, nullable=False)
    szn = Column('szn', Integer, nullable=False)
    date = Column('date', DATETIME, nullable=False)
    team = Column('team', String, primary_key=True, nullable=False)
    passing_cmp = Column('passing_cmp', Float, nullable=True, default=None)
    passing_att = Column('passing_att', Float, nullable=True, default=None)
    passing_cmp_prc = Column('passing_cmp_prc', Float, nullable=True, default=None)
    passing_yds = Column('passing_yds', Float, nullable=True, default=None)
    passing_tds = Column('passing_tds', Float, nullable=True, default=None)
    passing_int = Column('passing_int', Float, nullable=True, default=None)
    passing_rate = Column('passing_rate', Float, nullable=True, default=None)
    passing_sacks = Column('passing_sacks', Float, nullable=True, default=None)
    passing_sack_yds_lost = Column('passing_sack_yds_lost', Float, nullable=True, default=None)
    passing_yds_att = Column('passing_yds_att', Float, nullable=True, default=None)
    passing_net_yds_att = Column('passing_net_yds_att', Float, nullable=True, default=None)
    rushing_att = Column('rushing_att', Float, nullable=True, default=None)
    rushing_yds = Column('rushing_yds', Float, nullable=True, default=None)
    rushing_yds_att = Column('rushing_yds_att', Float, nullable=True, default=None)
    rushing_tds = Column('rushing_tds', Float, nullable=True, default=None)
    scoring_tds = Column('scoring_tds', Float, nullable=True, default=None)
    scoring_pts = Column('scoring_pts', Float, nullable=True, default=None)
    punts = Column('punts', Float, nullable=True, default=None)
    punt_yds = Column('punt_yds', Float, nullable=True, default=None)
    third_down_conv = Column('third_down_conv', Float, nullable=True, default=None)
    fourth_down_conv = Column('fourth_down_conv', Float, nullable=True, default=None)

    games = relationship('Game', back_populates='team_avg_stats')

class CareerTotals(Base):
    __tablename__ = 'career_totals'

    game_id = Column('game_id', Integer, ForeignKey('games.game_id'), primary_key=True, nullable=False)
    szn = Column('szn', Integer, nullable=False)
    date = Column('date', DATETIME, nullable=False)
    player_id = Column('player_id', Integer, ForeignKey('players.player_id'), primary_key=True, nullable=False)
    team = Column('team', String, nullable=False)
    passing_cmp = Column('passing_cmp', Integer, nullable=True, default=None)
    passing_att = Column('passing_att', Integer, nullable=True, default=None)
    passing_cmp_prc = Column('passing_cmp_prc', Float, nullable=True, default=None)
    passing_yds = Column('passing_yds', Integer, nullable=True, default=None)
    passing_tds = Column('passing_tds', Integer, nullable=True, default=None)
    passing_int = Column('passing_int', Integer, nullable=True, default=None)
    passing_rate = Column('passing_rate', Float, nullable=True, default=None)
    passing_sacks = Column('passing_sacks', Integer, nullable=True, default=None)
    passing_sack_yds_lost = Column('passing_sack_yds_lost', Integer, nullable=True, default=None)
    passing_yds_att = Column('passing_yds_att', Float, nullable=True, default=None)
    passing_adj_yds_att = Column('passing_adj_yds_att', Float, nullable=True, default=None)
    rushing_att = Column('rushing_att', Integer, nullable=True, default=None)
    rushing_yds = Column('rushing_yds', Integer, nullable=True, default=None)
    rushing_yds_att = Column('rushing_yds_att', Float, nullable=True, default=None)
    rushing_tds = Column('rushing_tds', Integer, nullable=True, default=None)
    scoring_tds = Column('scoring_tds', Integer, nullable=True, default=None)
    scoring_pts = Column('scoring_pts', Integer, nullable=True, default=None)
    receiving_rec = Column('receiving_rec', Integer, nullable=True, default=None)
    receiving_yds = Column('receiving_yds', Integer, nullable=True, default=None)
    receiving_yds_rec = Column('receiving_yds_rec', Float, nullable=True, default=None)
    receiving_tds = Column('receiving_tds', Integer, nullable=True, default=None)
    receiving_tgts = Column('receiving_tgts', Integer, nullable=True, default=None)
    receiving_catch_prc = Column('receiving_catch_prc', Float, nullable=True, default=None)
    receiving_yds_tgt = Column('receiving_yds_tgt', Float, nullable=True, default=None)
    fumbles_fmb = Column('fumbles_fmb', Integer, nullable=True, default=None)
    fumbles_fl = Column('fumbles_fl', Integer, nullable=True, default=None)

    player = relationship('Player', back_populates='career_totals')
    games = relationship('Game', back_populates='career_totals')