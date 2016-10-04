import tesorflow as tf
graph = tf.get_default_graph()
graph.get_opreations()
input_value = tf.constant(1.0)
operations = graph.get_operations()
operations[0].node_def

sess = tf.Session()
sess.run(input_value)

weight = tf.Variable(0.8)

for op in graph.get_operatinos(): print (op.name)

output_value = weight * input_value

op = graph.get_operations()[-1]


for op_input in op.inputs: print (op_input)

init = tf.initialize_all_variables()
sess.run(init)
sess.run(output_value)

x = tf.constant(1.0, name='input')
w = tf.Variable(0.8, name='weight')
y = tf.mul(w, x, name='output')
summary_writer = tf.train.SummaryWriter('log_simple_graph', sess.graph)

y_ = tf.constant(0.0)
loss = (y - y_)**2
optim = tf.train.GradientDescentOptimizer(learning_rate=0.025)

grads_and_vars = optim.compute_gradients(loss)
sess.run(tf.initialize_all_variables())
sess.run(grads_and_vars[1][0])
sess.run(optim.apply_gradients(grads_and_vars))
sess.run(w)
