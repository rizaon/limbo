class LimboServer(object):
    def __init__(self, slack, config, hooks, db, tg_bot):
        self.slack = slack
        self.config = config
        self.hooks = hooks
        self.db = db
        self.tg_bot = tg_bot

    def query(self, sql, *params):
        c = self.db.cursor()
        c.execute(sql, params)
        rows = c.fetchall()
        c.close()
        self.db.commit()
        return rows
