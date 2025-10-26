# Getting Started Guide: Your First Steps

## What You'll Need

### **Computer Requirements** 💻

- Any modern computer (Windows, Mac, or Linux)
- Python 3.9 or newer (free software for running the system)
- About 500 MB of free disk space
- Internet connection for initial setup

### **Your Data** 📁

- Excel or CSV file with equipment descriptions
- Column containing equipment descriptions (any name is fine)
- At least 10-20 sample descriptions to test with

### **Time Investment** ⏱️

- Initial setup: 30 minutes
- Learning the basics: 1 hour
- Getting comfortable: 1-2 days of occasional use

## Step-by-Step Installation

### **Step 1: Install Python** 🐍

If you don't have Python installed:

1. Go to python.org
2. Download Python 3.11 (or newer)
3. Install it (check "Add to PATH" during installation)

### **Step 2: Download the Equipment Classifier** 📥

1. Download the equipment_classifier folder
2. Put it somewhere easy to find (like your Desktop or Documents folder)

### **Step 3: Install the System** ⚙️

1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to the equipment_classifier folder
3. Type: `pip install -e .`
4. Wait for installation to complete (2-3 minutes)

### **Step 4: Test the Installation** ✅

Type: `python demo.py`

You should see something like:

```
Equipment Classification Demo
==================================================

Description: AHU 4.13 maintenance required
Equipment Type: AHU
Confidence: 0.683 (Medium)
Equipment ID: ahu 4.13
```

If you see this, congratulations! The system is working.

## Your First Classification

### **Try a Single Description**

Open Command Prompt and type:

```
equipment-classify --text "Elevator inspection needed" --industry AIRPORT
```

You'll get a result like:

```
Text: Elevator inspection needed
Equipment Type: ELEVATOR
Confidence: 0.633 (Medium)
```

### **Try Your Own Data**

1. Put your Excel file in the equipment_classifier folder
2. Run: `equipment-classify --file your_file.xlsx --industry AIRPORT --output results.xlsx`
3. Open results.xlsx to see all your classifications

## Understanding the Results

### **Equipment Type** 🏷️

This is what the system thinks your equipment is:

- **AHU**: Air Handling Unit (heating/cooling)
- **ELEVATOR**: Vertical transportation
- **PUMP**: Pumping equipment
- **CHILLER**: Cooling equipment
- **OTHER**: Couldn't determine specific type

### **Confidence Score** 📊

This tells you how sure the system is:

- **0.7+ (High)**: Very confident - likely correct
- **0.5-0.7 (Medium)**: Reasonable guess - probably right
- **Under 0.5 (Low)**: Not sure - human should double-check

### **Equipment ID** 🆔

If found, this is the specific equipment identifier:

- "AHU 4.13" from "AHU 4.13 needs repair"
- "Elevator #8" from "Main elevator #8 broken"

## Industries You Can Choose From

### **AIRPORT** ✈️

Best for: Airports, terminals, aviation facilities
Recognizes: AHUs, elevators, jet bridges, baggage systems, security equipment

### **CHEMICAL** ⚗️

Best for: Chemical plants, refineries, processing facilities
Recognizes: Reactors, pumps, heat exchangers, safety systems

### **MANUFACTURING** 🏭

Best for: Factories, production facilities, assembly plants  
Recognizes: Conveyors, robots, assembly equipment, production machinery

### **WATER** 💧

Best for: Water treatment plants, wastewater facilities, utilities
Recognizes: Pumps, filtration systems, treatment equipment

### **No Industry (Generic)** 🏢

Best for: Office buildings, schools, hospitals, mixed facilities
Recognizes: Basic HVAC, electrical, plumbing, building systems

## Common Questions and Solutions

### **"The confidence scores seem low"**

This is normal! The system is conservative and honest about uncertainty. Scores above 0.5 are usually reliable, and scores above 0.7 are very reliable.

### **"It's not recognizing my equipment"**

Try different industry settings, or the equipment might need to be added to the system's vocabulary.

### **"Some results say 'OTHER'"**

This happens when:

- The description is about a location, not equipment
- The equipment type isn't in the system's vocabulary yet
- The description is too vague or unclear

### **"My Excel file won't load"**

Make sure:

- File is .xlsx or .csv format
- No spaces or special characters in the filename
- File isn't open in Excel while you're trying to use it

## Tips for Better Results

### **Writing Better Descriptions** ✍️

**Good:** "AHU 4.13 preventive maintenance required"
**Bad:** "Thing in Room 205 is broken"

**Good:** "Chiller unit making loud noise"  
**Bad:** "Loud noise somewhere"

### **Choosing the Right Industry** 🎯

Use the industry setting that best matches your facility. When in doubt, try different settings and see which gives better results.

### **Interpreting Confidence** 🤔

- Use high-confidence results as-is
- Review medium-confidence results occasionally
- Always check low-confidence results manually

### **Working with Large Files** 📈

For files with thousands of rows:

1. Test with a small sample first (50-100 rows)
2. Adjust settings based on the test results
3. Process the full file once you're satisfied

## Next Steps: Getting More Advanced

### **Week 1: Basic Usage**

- Classify your existing work orders
- Get familiar with confidence scores
- Learn which industry setting works best

### **Week 2: Integration**

- Set up regular processing of new work orders
- Create reports showing equipment type distribution
- Train your team on interpreting results

### **Month 1: Optimization**

- Fine-tune confidence thresholds
- Add facility-specific equipment terms
- Set up automated workflows

### **Ongoing: Analysis**

- Track maintenance patterns by equipment type
- Use data to improve maintenance planning
- Generate regular analytical reports

## Getting Help

### **Built-in Help** 📚

Type `equipment-classify --help` to see all available options

### **Example Files** 📄

Look in the equipment_classifier folder for:

- `demo.py`: Basic examples
- `claude_skill_example.py`: Advanced usage
- Test files with sample data

### **Common Commands** 💻

```bash
# Classify single text
equipment-classify --text "Your description here"

# Process Excel file
equipment-classify --file data.xlsx --output results.xlsx

# Use specific industry
equipment-classify --file data.xlsx --industry AIRPORT

# Only show high-confidence results
equipment-classify --file data.xlsx --confidence 0.7
```

## Success Checklist ✅

After your first week, you should be able to:

- [ ] Install and run the system
- [ ] Classify single equipment descriptions
- [ ] Process an Excel file of work orders
- [ ] Understand confidence scores
- [ ] Choose appropriate industry settings
- [ ] Interpret the results
- [ ] Generate basic reports

Remember: This system is designed to help you, not replace your expertise. Use it as a smart assistant that handles the routine work so you can focus on the complex decisions that require human judgment.
