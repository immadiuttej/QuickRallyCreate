from pyral import Rally
import pandas as pd
import numpy as np
from datetime import datetime

def create_user_stories_and_tasks(server, apikey, workspace, project, username, file):
    try:
        rally = Rally(server=server, apikey=apikey, workspace=workspace, project=project)
        project_ref = rally.getProject()
        default_user_ref = rally.getUserInfo(username=username).pop(0)
        
        df = pd.read_excel(file)
        
        required_columns = [
            'User Story or Task', 'Name', 'Description', 'Plan Estimate', 
            'Todo Hours', 'Estimate Hours', 'Release', 'Iteration', 
            'Development End Date', 'Owner'
        ]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Excel file must contain columns: {', '.join(required_columns)}")
        
        string_columns = ['User Story or Task', 'Name', 'Description', 'Release', 'Iteration', 'Owner']
        for col in string_columns:
            df[col] = df[col].fillna('')
        
        numeric_columns = ['Plan Estimate', 'Todo Hours', 'Estimate Hours']
        for col in numeric_columns:
            df[col] = df[col].replace({np.nan: None})
        
        df['Development End Date'] = pd.to_datetime(df['Development End Date'], format='%m/%d/%Y', errors='coerce')
        
        # Process all unique owners
        unique_owners = df['Owner'].unique()
        owner_refs = {}
        for owner in unique_owners:
            if owner:
                try:
                    owner_ref = rally.getUserInfo(username=owner).pop(0).ref
                    owner_refs[owner] = owner_ref
                except IndexError:
                    # If the owner is not found, we'll use the default owner
                    owner_refs[owner] = default_user_ref.ref
        
        stories = []
        current_story = None
        
        for _, row in df.iterrows():
            if row['User Story or Task'].lower() == 'user story':
                if current_story:
                    stories.append(current_story)
                
                current_story = {
                    "Project": project_ref.ref,
                    "Name": row['Name'].strip(),
                    "Description": row['Description'],
                    "Owner": owner_refs.get(row['Owner'], default_user_ref.ref),
                    "ScheduleState": "Defined",
                    "PlanEstimate": row['Plan Estimate'],
                    "Release": row['Release'],
                    "Iteration": row['Iteration'],
                    "DevelopmentEndDate": row['Development End Date'].strftime('%Y-%m-%d') if pd.notnull(row['Development End Date']) else None,
                    "Tasks": []
                }
            elif row['User Story or Task'].lower() == 'task':
                if not current_story:
                    raise ValueError("Task found before a user story was defined")
                
                task_data = {
                    "Name": row['Name'],
                    "ToDo": row['Todo Hours'],
                    "Estimate": row['Estimate Hours'],
                    "Owner": owner_refs.get(row['Owner'], current_story['Owner'])  # Use task owner if specified, otherwise use story owner
                }
                current_story['Tasks'].append(task_data)
            else:
                raise ValueError(f"Invalid value in 'User Story or Task' column: {row['User Story or Task']}")
        
        if current_story:
            stories.append(current_story)
        
        for story in stories:
            story_data = {
                "Project": story["Project"],
                "Name": story["Name"],
                "Description": story["Description"],
                "Owner": story["Owner"],
                "ScheduleState": story["ScheduleState"],
                "PlanEstimate": story["PlanEstimate"],
                "DevelopmentEndDate": story["DevelopmentEndDate"]
            }
            
            if story["Release"]:
                release = rally.get('Release', query=f'Name = "{story["Release"]}"', instance=True)
                if release:
                    story_data["Release"] = release.ref
            
            if story["Iteration"]:
                iteration = rally.get('Iteration', query=f'Name = "{story["Iteration"]}"', instance=True)
                if iteration:
                    story_data["Iteration"] = iteration.ref
            
            created_story = rally.put('HierarchicalRequirement', story_data)
            
            if hasattr(created_story, 'ref'):
                for task in story['Tasks']:
                    task_data = {
                        "Project": project_ref.ref,
                        "WorkProduct": created_story.ref,
                        "Name": task['Name'],
                        "Owner": task['Owner'],  # Use the task-specific owner
                        "State": "Defined",
                        "ToDo": task['ToDo'],
                        "Estimate": task['Estimate']
                    }
                    rally.put('Task', task_data)
        
        return "Success"
    except Exception as e:
        return f"Failed Creation For Reasons: {str(e)}. Please re-try!"