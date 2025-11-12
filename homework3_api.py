"""
Jiajie Lin
DS 3500 Homework 3 API
The primary API for interacting with the league dataset
"""
import pandas as pd
import numpy as np
import sankey as sk
import matplotlib.pyplot as plt


class LeagueAPI():

    def load_league(self, filename):
        #Loads and stores the league Data
        self.league = pd.read_csv(filename)

    def get_tier(self):
        """Gets the tier(rank) of the players """
        tier = self.league.tier.unique()
        return (tier)

    def extract_local_network(self,tier,action):
        """
        connects the ranks to number of wins(grouped by standard deviation up to +- 2 standard deviations)
        and links it by number of players
        """
        league = self.league

        result = league.groupby(['tier',action]).size().reset_index(name = 'player_count')

        return result

    def veteran_players(self,tier,action):
        """
        collects the data of people who are veteran players
        """
        league = self.league

        result = league[league['veteran'] == True]

        result = result.groupby([tier, action]).size().reset_index(name="player_count")

        return result

    def bk(self,action):
        data_set = self.league

        fig, ax = plt.subplots(figsize = (10,6))
        ax.boxplot(data_set[action])
        ax.set_title(f'{action}')

        plt.close()
        return fig


def main():
    league_api = LeagueAPI()
    league_api.load_league('cleaned_league.csv')

    tiers = league_api.get_tier()
    network = league_api.extract_local_network('tier','losses_SD')
    league_api.veteran_players('tier','wins')


if __name__ == "__main__":
    main()