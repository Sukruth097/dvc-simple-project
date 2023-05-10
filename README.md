dvc-simple-project-template-main


# Project Components Architecture
```
                  +-----------+           
                  | load_data |           
                  +-----------+           
                        *                 
                        *                 
                        *                 
                  +------------+          
                  | split_data |          
                  +------------+          
                ***            ***        
              **                  ***     
            **                       **   
+----------------+                     ** 
| model_training |                   **   
+----------------+                ***     
                ***            ***        
                   **        **           
                     **    **             
              +------------------+        
              | model_evaluation |        
              +------------------+        
```
