import tiktoken

#this function counts the number of tokens in a string
def count_tokens(content: str, model: str) -> int:    
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(content)
    return len(tokens)

# this function can truncate a string
def truncate_string(content: str, model: str, token_length: int) -> str:            
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(content)
    return encoding.decode(tokens[:token_length])
    

# delete this
# this is done to combine multiple messages into one request so that RPM and RPD is maintained
# def combine_in_same_message(contents: list[str], model: str, token_length: int):
#     print("TODO: IMPLEMENT combine_in_same_message")
#     combined_msg = ""    
#     combined_tcount = 0
#     current_content_counter = 0 # TODO: remove this code. this is only for debugging    

#     msg_counter = 0


#     for msg in contents:        
#         tcount = count_tokens(msg, model)
#         if tcount + combined_tcount < token_length:
#             combined_msg = "".join() #combined_msg + ",\n"+msg            
#             combined_tcount += tcount
#             current_content_counter += 1 # TODO: remove this line. it is for debug ONLY
#         else:
#             res = combined_msg            
#             # reset                        
#             combined_msg = ""
#             combined_tcount = 0
#                 # print("# of digested messages in this batch %d" % current_content_counter) # TODO: remove this line. it is only for debugging
#                 # current_content_counter = 0 # TODO: remove this line. it is only for debugging            

#             yield res
#     yield combined_msg 
