import vessel_scoring.add_measures

class BaseModel(object):
    # def train_on_messages(self, messages):
    #     messages = AddMeasures(messages, self.windows)        
    #     y_train = utils.is_fishy(train_data)
    #     model.fit(train_data, y_train)
    #     return model

    def predict_messages(self, messages):
        for message in AddMeasures(messages, self.windows):
            msg['measure_new_score'] = float(self.model.predict_proba({
                        key: [value]
                        for key, value in msg.iteritems()
                        })[0][1])
            yield msg
        
    def dump_arg_dict(self):
        return {}

    def dump_dict(self):
        model_class = type(self)
        return {'model': "%s.%s" % (model_class.__module__, model_class.__name__),
                'args': self.dump_arg_dict(),
                }

