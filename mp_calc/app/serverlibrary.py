def merge(array,start_i: int, middle_i: int, end_i: int,byfunc):
    n_left = middle_i - start_i+ 1
    n_right = end_i - middle_i
    left_array = array[start_i:middle_i+1]    
    right_array = array[middle_i+1:end_i+1]
    left_pointer = 0
    right_pointer = 0
    destination = start_i
    while left_pointer < n_left and right_pointer < n_right:
        if (byfunc)(left_array[left_pointer]) <= (byfunc)(right_array[right_pointer]):
            array[destination] = left_array[left_pointer]
            left_pointer += 1
        else:
            array[destination] = right_array[right_pointer]
            right_pointer += 1
        destination += 1
    while left_pointer < n_left and right_pointer >= n_right:
        array[destination] = left_array[left_pointer]
        left_pointer += 1
        destination += 1
    while right_pointer < n_right and left_pointer >= n_left:
        array[destination] = right_array[right_pointer]
        right_pointer += 1
        destination += 1

def mergesort_recursive(array: list, start_i: int, end_i: int,byfunc) -> None:
    if (end_i - start_i > 0):
        middle_i = (start_i+end_i)//2
        mergesort_recursive(array,start_i,middle_i,byfunc) 
        mergesort_recursive(array,middle_i+1,end_i,byfunc) 
        merge(array,start_i,middle_i,end_i,byfunc) 
    return array

def mergesort(array,byfunc=None):
    start_i = 0
    end_i = len(array) -1
    mergesort_recursive(array,start_i,end_i,byfunc)
    return array

class Stack:
  def __init__(self) -> None:
      self.__items= []

  @property
  def is_empty(self) -> bool:
      if len(self.__items) == 0:
          return True
      else:
          return False

  @property
  def size(self):
      return len(self.__items)
      
  def push(self, item):
      return self.__items.append(item)

  def pop(self):
      if self.is_empty:
          return None
      else:
          to_pop = self.__items[-1]
          self.__items.pop()
          return to_pop

  def peek(self):
      if self.is_empty==True:
          return None
      else:
          return self.__items[-1]

class EvaluateExpression:
  valid_char = '0123456789+-*/() '
  operator = '+-*/()'
  def __init__(self,string = ""):
    self._str = string

  @property
  def expression(self):
    return self._str

  @expression.setter
  def expression(self, new_expr):
    self._str = ""
    for i in new_expr:
      if i not in self.valid_char:
        self._str = ""
        break
      else:
        self._str += i

  def insert_space(self):
    output = ""
    for i in self._str:
      if i in self.operator:
        output += " {} ".format(i)
      else:
        output += i
    return output
  

  def process_operator(self, operand_stack, operator_stack):
    top_number = operand_stack.pop()
    bottom_number = operand_stack.pop()
    operator = operator_stack.pop()
    if operator == "+":
      operand_stack.push(top_number+bottom_number)
    elif operator == "*":
      operand_stack.push(top_number*bottom_number)    
    elif operator == "-":
      operand_stack.push(bottom_number-top_number)
    elif operator == "/":
      operand_stack.push(bottom_number//top_number)

  def evaluate(self):
    operand_stack = Stack()
    operator_stack = Stack()
    expression = self.insert_space()
    tokens = expression.split()
    for i in tokens:
      if i not in self.operator:
        operand_stack.push(int(i))
      elif i == "+" or i == "-":
        if operator_stack.is_empty == False and operator_stack.peek() != "(" and operator_stack.peek() != ")" and operand_stack.size > 1:
          self.process_operator(operand_stack,operator_stack)
        operator_stack.push(i)
      elif i == "*" or i == "/":
        if operator_stack.is_empty == False and (operator_stack.peek() == "*" or operator_stack.peek() == "/") and operand_stack.size > 1:
          self.process_operator(operand_stack,operator_stack)
        operator_stack.push(i)
      elif i == "(":
        operator_stack.push(i)
      elif i == ")":
        while operator_stack.peek() != "(":
          self.process_operator(operand_stack,operator_stack)
        operator_stack.pop()
    
        

    while operator_stack.is_empty == False:
      self.process_operator(operand_stack,operator_stack)
    
    return operand_stack.peek()


def get_smallest_three(challenge):
  records = challenge.records
  times = [r for r in records]
  mergesort(times, lambda x: x.elapsed_time)
  return times[:3]





