from tkinter import E
from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake

class Blockchain():
  def __init__(self):
    self.blocks = [Block.genesis()]
    self.accountModel = AccountModel()
    self.pos = ProofOfStake()
  
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
    if transaction.type == 'STAKE':
      sender = transaction.senderPublicKey
      receiver = transaction.receiverPublicKey
      if sender == receiver:
        amount = transaction.amount
        self.pos.update(sender, amount)
        self.accountModel.updateBalance(sender, -amount)
      else:
        sender = transaction.senderPublicKey
        receiver = transaction.receiverPublicKey
        amount = transaction.amount
        self.accountModel.updateBalances(sender, -amount)
        self.accountModel.updateBalances(receiver, amount)
    
  def nextForger(self):
    lastBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
    nextForger = self.pos.forger(lastBlockHash)
    return nextForger
  
  def createBlock(self, transactionFromPool, forgerWallet):
    coveredTransactions = self.getCoveredTransactionSet(transactionFromPool)
    self.executeTransactions(coveredTransactions)
    newBlock = forgerWallet.createBlock(coveredTransactions, BlockchainUtils.hash(
      self.blocks[-1].payload()).hexdigest(), len(self.blocks))
    self.blocks.append(newBlock)
    return newBlock
  
  def transactionExists(self, transaction):
    for block in self.blocks:
      for blockTransaction in block.transactions:
        if blockTransaction.equals(transaction):
          return True
    return False
  
  def forgerValid(self, block):
    forgerPublicKey = self.pos.forger(block.lastHash)
    proposedBlockForger = block.forger
    if forgerPublicKey == proposedBlockForger:
      return True
    else:
      return False
    
  def transactionValid(self, transactions):
    coveredTransactions = self.getCoveredTransactionSet(transactions)
    if len(coveredTransactions) == len(transactions):
      return True
    return False