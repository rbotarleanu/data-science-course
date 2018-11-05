import tensorflow as tf

class LinearRegressionTF:

    def __init__(self, reg=0.):
        self.coef_ = None
        self.intercept_ = None
        self.reg = reg

    def fit(self, X, y):
        self._fit(X, y)

    def _fit(self, X, y):
        y = tf.cast(tf.reshape(y, (-1, 1)), dtype=tf.float32)
        X = tf.concat([X, tf.ones((X.shape[0], 1), dtype=tf.float32)], axis=1) # add the intercept
        # theta = (X.t %*% X - reg*I)^-1 * X.t * y
        n = int(X.shape[1])
        mreg = self.reg * tf.eye(n, n)
        theta = tf.matmul(
                    tf.matmul(
                        tf.linalg.inv(
                            1/n * tf.matmul(tf.transpose(X), X) + mreg
                        ),
                        1/n * tf.transpose(X)),
                    y)

        self.intercept_ = theta[-1]
        self.coef_ = theta[:-1]        

    def predict(self, X):
        return tf.matmul(tf.cast(X, dtype=tf.float32), self.coef_) + self.intercept_
