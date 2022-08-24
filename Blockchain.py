from tkinter import E
from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel

class Blockchain():
  def __init__(self):
    self.blocks = [Block.genesis()]
    self.accountModel = AccountModel()
  
  def addBlock(self, newBlock):
    self.executeTransactions(newBlock.transactions)
    self.blocks.append(newBlock)
    
  def toJson(self):
    data = {}
    jsonBlocks = []
    for block in self.blocks:
      jsonBlocks.append(block.toJson())
    data['blocks'] = jsonBlocks
    return data

  def blockCountValid(self, block):
    if self.blocks[-1].blockCount == block.blockCount - 1:
      return True
    else:
      return False
    
  def lastBlockHashValid(self, block):
    latestBlockchainBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()

    if latestBlockchainBlockHash == block.lastHash:
      return True
    else: 
      return False
  
  def getCoveredTransactionSet(self, transactions):
    coveredTransactions = []
    for transaction in transactions:
      if self.transactionCovered(transaction):
        coveredTransactions.append(transaction)
      else:
        print('Transaction not covered')
    return coveredTransactions
  
  def transactionCovered(self, transaction):
    if(transaction.type == 'EXCHANGE'):
      return True
    senderBalance = self.accountModel.getBalances(transaction.senderPublicKey)
    if senderBalance >= transaction.amount:
      return True
    else:
      return False
    
  def executeTransactions(self, transactions):
    for transaction in transactions:
      self.executeTransaction(transaction)
    
  def executeTransaction(self, transaction):
    sender = transaction.senderPublicKey
    receiver = transaction.receiverPublicKey
    amount = transaction.amount
    self.accountModel.updateBalances(sender, -amount)
    self.accountModel.updateBalances(receiver, amount)