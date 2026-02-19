# AI Assignment 01 - Kids in the Yard

## Comparison
1. Which tool(s) did you use?
   
   I used an LLM (Specifically ChatGPT Model 5.2) for comparison with my implementation.
   
2. If you used an LLM, what was your prompt to the LLM?

   I gave it screenshots of the Assignment PDF (the parts about the implementation itself and what the code should do, the example provided of how the code should run, and the sample design given). I gave screenshots because I think a good prompt for an LLM should have both images and text (atleast what to code itself can be better explained through the the pdf). I followed up by sending it all of the csv files (except the one for CS 562) and asked it to consider these in the code.
   
   My prompt itself was: "This is a Python program. Read through these screenshots of what the code should contain, an example screenshot of how it should run and the potential inputs and outputs and make sure all of the code follows the coding style of PEP8 as shown in the last image. I have also attached all of the csv files that will be used for this so that you can consider them in your code. Make sure to code each class as a separate file (so in your case, in separate Python markdown code blocks) and include an extra file for any sort of helper functions that you think could be required.
Note: Make sure you do not use any external/in-built libraries (with exceptions of Random, Pandas and OS)."
 
3. What differences are there between your implementation and the LLM?

   The LLM's code always picks descendants from the 2 founder last names (self.founder_last_names) instead of choosing from one of the parents (which mine does). The LLM's code forces 2 founders to be partners every time without considering the "marriage_rate" to decide partners. It uses a function "random.randint(min, max) to decide the # of children while mine calculates it using the birth rate. It also adds some extra helper functions "is_int_like, "safe_float", "maybe" which I don't think do anything useful. It also has a complex counting method for the decades and duplicates etc.

4. What changes would you make to your implementation in general based on suggestions from the LLM?

   The main changes I would make are related to user inputs: making the output to the user clearer and more clean, keeping error messages consistent/avoiding large error tracebacks and making the interaction loop more flexible and robust to invalid inputs. I could make use of its methods for duplicates and decade counting because they were solid and properly accounting for any twist in the data while mine is through simple dictionary counting. I could also work in keeping all of the printing logic in one page (while that overcomplicates some other aspects, it keeps the output to the user clear) instead of scattering them across the various .py files made.

5. What changes would you refuse to make?

   
