from MyClass import *
from mytools2 import read_index, byteMatrix
import time
import sys

def main(num_file):
    d = 3
    kms = KMS(d)
    broker = Broker()
    requester = kms.KeyGen(broker, "100", False)
    worker = kms.KeyGen(broker, '0')

    print("Setup finish")
    print("SKeyGen finish")

    f_index = []
    word_space = read_index(num_file)
    start = time.clock()
    for i,w in enumerate(word_space):
        worker.IntEnc(w)
        print('index {}'.format(i))
        broker.IntTran(worker.id, worker.I_star)
        f_index.append(broker.I_tilde)

        temp = kms.M1.Copy()
        temp.Transpose()

        # print(temp*worker.I_ab[0][0])
        # print(broker.I_tilde[0][0])
    end = time.clock()
    time_use = end-start
    print("document:{}".format(len(word_space)))
    print('time:{}'.format(time_use))
    index_mem_use = 0
    #索引
    for I_tilde in f_index:
        for word in I_tilde:
            # index_mem_use += len(pickle.dumps(word[0].data)) + sys.getsizeof(word[0])
            # index_mem_use += len(pickle.dumps(word[1].data)) + sys.getsizeof(word[1])
            index_mem_use += byteMatrix(word[0])
            index_mem_use += byteMatrix(word[1])#0.10348892211914062M

    print('memory:{}M'.format(index_mem_use/1024/1024))
    print('index construction complete')

    while(True):
        q = input()

        Q = [q]
        requester.TdGen(Q)
        broker.TdTran(requester.id, requester.T)
        # print(kms.M1.Inverse() * requester.Q_ab[0])
        # print(broker.T_tilde[0])
        # print(test_Q_I(requester.Q_vector, worker.I[0]))
        result = []
        start = time.clock()
        for doc_id, I_tilde in enumerate(f_index):
            broker.I_tilde = I_tilde
            if broker.Match() == 1:
                result.append(doc_id)
                print(doc_id)
        end = time.clock()
        print("time_used:{}, doc_num:{}".format((end-start), len(result)))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        input_lines_num = 50
    else:
        input_lines_num = int(sys.argv[1])
        if input_lines_num == 0:
            input_lines_num = 50
    main(input_lines_num)