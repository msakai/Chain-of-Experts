from experts.base_expert import BaseExpert

from langchain import PromptTemplate, OpenAI, LLMChain


class CodeReviewer(BaseExpert):

    ROLE_DESCRIPTION = 'You are a code reviewer that conducts thorough reviews of the implemented code to identify any errors, inef- ficiencies, or areas for improvement.'
    FORWARD_TASK = '''As a Code Reviewer, your responsibility is to conduct thorough reviews of implemented code related to optimization problems. 
You will identify possible errors, inefficiencies, or areas for improvement in the code, ensuring that it adheres to best practices and delivers optimal results. Now, here is the problem: 
{problem_description}. 

You are supposed to refer to the comments given by your colleagues from other aspects: {comments_text}'''

    BACKWARD_TASK = '''When you are solving a problem, you get a feedback from the external environment. You need to judge whether this is a problem caused by you or by other experts (other experts have given some results before you). If it is your problem, you need to give Come up with solutions and refined code.

The original problem is as follow:
{problem_description}

The answer you give previously is as follow:
{previous_answer}
    
The feedback is as follow:
{feedback}

The output format is a JSON structure followed by refined code:
{{
    'is_caused_by_you': false,
    'reason': 'leave empty string if the problem is not caused by you',
    'refined_result': 'Your refined answer...'
}}
'''

    def __init__(self, model):
        super().__init__(
            name='Code Reviewer',
            description='Skilled in programming and coding, capable of implementing the optimization solution in a programming language.',
            model=model   
        )

    def forward(self, problem, comment_pool):
        self.problem = problem
        comments_text = comment_pool.get_current_comment_text()
        output = self.forward_chain.predict(
            problem_description=problem['description'], 
            comments_text=comments_text
        )
        self.previous_code = output
        return output

    def backward(self, feedback_pool):
        if not hasattr(self, 'problem'):
            raise NotImplementedError('Please call foward first!')
        output = self.backward_chain.predict(
            problem_description=self.problem['description'], 
            previous_answer=self.previous_code,
            feedback=feedback_pool.get_current_comment_text())
        return output
