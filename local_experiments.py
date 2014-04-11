from models import local_dev_model

res = local_dev_model.run_simulation(10)

import matplotlib.pyplot as plt

plt.figure()
plt.title("Locality and Effort")
plt.hold(True)
plt.plot(res['efforts'])
plt.plot(res['high_statuses'])

plt.legend(["Agents Making Effort", "Attaining High Status"], loc="best")

plt.show()