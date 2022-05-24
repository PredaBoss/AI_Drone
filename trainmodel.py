import torch
import matplotlib.pyplot as plt

import myModel

# we set up the lossFunction as the mean square error
lossFunction = torch.nn.MSELoss()

# we create the ANN
ann = myModel.Net(n_feature=2, n_hidden=100, n_output=1).double()
data = torch.load("mydataset.dat")
print(ann)

# we use an optimizer that implements stochastic gradient descent
optimizer_batch = torch.optim.SGD(ann.parameters(), lr=0.002)

# we memorize the losses forsome graphics
loss_list = []
avg_loss_list = []

# we set up the environment for training in batches
batch_size = 16
n_batches = int(len(data) // batch_size)
print("Number of batches:", n_batches)

x = torch.tensor([(item[0], item[1]) for item in data])
y = torch.unsqueeze(torch.tensor([item[2] for item in data]), dim=1)

splitX = torch.split(x, batch_size)
splitY = torch.split(y, batch_size)

for epoch in range(2000):

    for batch in range(n_batches):
        # we prepare the current batch  -- please observe the slicing for tensors
        batch_X, batch_y = splitX[batch].double(), splitY[batch].double()

        # we compute the output for this batch
        prediction = ann(batch_X)

        # we compute the loss for this batch
        loss = lossFunction(prediction, batch_y)

        # we save it for graphics
        loss_list.append(loss.item())

        # we set up the gradients for the weights to zero (important in pytorch)
        optimizer_batch.zero_grad()

        # we compute automatically the variation for each weight (and bias) of the network
        loss.backward()

        # we compute the new values for the weights
        optimizer_batch.step()

    # we print the loss for all the dataset for each 100th epoch
    if epoch % 100 == 99:
        y_pred = ann(x.double())
        loss = lossFunction(y_pred, y.double())
        print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))



    # Specify a path
filepath = "myNetwork.pt"

# save the model to file
torch.save(ann.state_dict(), filepath)

plt.plot(loss_list)
plt.savefig("loss.png")


# visualise the parameters for the ann (aka weights and biases)
# for name, param in ann.named_parameters():
#     if param.requires_grad:
#         print (name, param.data)
