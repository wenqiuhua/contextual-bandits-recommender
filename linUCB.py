from _commons import warn, error, create_dir_path
import numpy as np

class LinUCB:
    def __init__(self, alpha, dataset):
        self.dataset = dataset
        self.alpha = alpha
        self.d = dataset.arm_feature_dim
        self.A = np.zeros(shape=(dataset.num_items, self.d, self.d)) # set of arms is not changing over time
        self.b = np.zeros(shape=(dataset.num_items, self.d))

        for a in range(self.A.shape[0]):
            self.A[a] = np.identity(self.d, dtype=self.A.dtype)

    def choose_arm(self, t):
        A = self.A
        b = self.b
        arm_features = self.dataset.get_features_of_current_arms(t=t)
        p_t = np.zeros(shape=(arm_features.shape[0],), dtype=float)
        for a in range(arm_features.shape[0]):
            x_ta = arm_features[a]
            A_a_inv = np.linalg.inv(A[a])
            theta_a = A_a_inv.dot(b[a])
            p_t[a] = theta_a.T.dot(x_ta) + self.alpha*np.sqrt(x_ta.T.dot(A_a_inv).dot(x_ta))

        max_idxs = np.argwhere(p_t == np.max(p_t)) #I want to randomly break ties, np.argmax return the first occurence of maximum.
        a_t = np.random.choice(max_idxs) #idx of article to recommend to user t

        r_t = self.dataset.recommend(user_id=t, item_id=a_t)

        x_t_at = arm_features[a_t]
        A[a_t] = A[a_t] + x_t_at.dot(x_t_at.T)
        b[a_t] = b[a_t] + r_t*x_t_at