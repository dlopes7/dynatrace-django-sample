import oneagent


class DynatraceQueryWrapper:

    db_info = None
    sdk = None

    def __init__(self):
        oneagent.initialize()

        if self.sdk is None:
            self.sdk = oneagent.get_sdk()

        if self. db_info is None:
            self.db_info = self.sdk.create_database_info('Polls',
                                                                   oneagent.sdk.DatabaseVendor.SQLITE,
                                                                   oneagent.sdk.Channel(oneagent.sdk.ChannelType.TCP_IP,
                                                                                        '127.0.0.1:6666'))

    def __call__(self, execute, sql, params, many, context):
        curremt_query = {'sql': sql, 'params': params, 'many': many}

        with self.sdk.trace_sql_database_request(self.db_info, curremt_query['sql']) as tracer:
            try:
                result = execute(sql, params, many, context)
            except Exception as e:
                tracer.mark_failed(e.__class__.__name__, str(e))
                raise
            else:
                return result


