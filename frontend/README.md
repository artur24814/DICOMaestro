# DICOMaestro Frontend

## Setup (React):
* Navigate to the frontend directory:
    ```bash
    cd ../frontend
    ```
* Install dependencies:
    ```bash
    npm install
    ```
* Start the development server:
    ```bash
    npm start
    ```
## Usage

Open your browser and navigate to `http://localhost:3000`.

## Adding New Tools to the Canvas (Frontend):
The frontend of DICOMaestro includes a canvas where users can interact with DICOM images and sequences. To extend the functionality of this canvas, you can create new tools that manipulate the images, such as drawing lines, rectangles, or other shapes.

To add new tools, follow these steps:

### Step 1: Understand the Tool Structure
Tools inherit from base classes:

* DrawingTool: Base class for tools that handle freeform drawing (e.g., lines, shapes).
* ShapeTool (optional): A subclass of DrawingTool for tools that work with geometric shapes like rectangles, circles, etc.
### Step 2: Create a New Tool
1. Decide the Type of Tool:

* For freeform drawing tools, extend DrawingTool.
* For shape-based tools (rectangles, circles, etc.), extend ShapeTool.

2. Implement Your Tool:

* Create a new file for the tool in the `components/` directory.
* Implement the required methods: `onMouseDown`, `onMouseMove`, `onMouseUp`, and optionally `onMouseOut`.
* Use the `color` property for tool styling.
Example: Triangle Tool

```javascript
import ShapeTool from './abstractions/ShapeToolABC';

class TriangleTool extends ShapeTool {
  constructor(color = 'black', , lineWidth = 1) {
    super(color, lineWidth)
  }

  drawShape(offsetX, offsetY, ctx) {
    const { x: startX, y: startY } = this.startPoint

    ctx.beginPath()
    ctx.moveTo(startX, startY)
    ctx.lineTo(offsetX, startY) // Horizontal line
    ctx.lineTo((startX + offsetX) / 2, offsetY) // Apex of the triangle
    ctx.closePath()
    ctx.strokeStyle = this.color
    ctx.stroke()
  }
}

export default TriangleTool
```
### Step 3: Register Your Tool in the ToolBarComponent.js
Import the Tool: In the component or manager that handles tool selection:

```javascript
import TriangleTool from '../../../components/TriangleTool'
```
Add Tool to the UI: Add buttons or menu items to allow users to select your tool:

```javascript
<Nav className='me-auto'>
  <div className='vr text-white' />
  <Nav.Link onClick={() => handleSelectTool(new DrawTool())}>
    <FaPen />
  </Nav.Link>
  <Nav.Link onClick={() => handleSelectTool(new PaintTool())}>
    <FaPaintbrush />
  </Nav.Link>
  <Nav.Link onClick={() => handleSelectTool(new LineTool())}>
    <LuPencilLine />
  </Nav.Link>
  <Nav.Link onClick={() => handleSelectTool(new RectangleTool())}>
    <BiRectangle />
  </Nav.Link>
  <Nav.Link onClick={() => handleSelectTool(new TriangleTool())}> // Add Here your class
    <BiTriangle /> // Add here icon
  </Nav.Link>
</Nav>
```

### Step 4: Test Your Tool
* Ensure the tool functions correctly in the canvas:
    * It should draw the intended shape or line.
    * Verify interactions with undo/redo functionality and proper behavior on onMouseOut.
### Step 5: Submit Your Changes
1. Write Tests (if applicable): Make sure the new tool is covered by tests.

2. Submit a Pull Request: Fork the repository, make your changes, and submit a pull request.

## Introduction to Memento Pattern in Our Application
In our application, we use the `Memento Design Pattern` to manage and preserve the state of various components over time, such as text inputs, images, or other interactive elements. The `Memento Pattern` allows us to save and restore the state of a component, enabling undo and redo functionality, and providing a seamless experience for users when they need to revert or reapply changes.

To implement this pattern, we've created a Memento Context Manager that is integrated with React Query for efficient state management and caching. The Memento Context stores the state of various components, and it is globally accessible across the entire application. This means that any component can save, undo, redo, and retrieve state changes without needing to manage its own state independently.

By leveraging `React Query's cach`e and the `Memento Manager`, we ensure that our application maintains a centralized and consistent state, with the ability to restore previous states even after page reloads or re-renders.

### Example Usage of Memento in a TextArea Component
With the `Memento Context` already set up in our app, you can easily integrate it into your components to track and manage state. Below is an example that shows how you can use the memento manager to implement undo and redo functionality for a simple `textarea` component:

```javascript
import React, { useState } from 'react'
import { useMemento } from '../../../contexts/MementoContext/MementoContext'

const TextAreaWithMemento = ({mementoName = 'textAreaMemento'}) => {
  const { saveMemento, undoMemento, redoMemento, currentMementoState } = useMemento()
  const [text, setText] = useState('')
  
  // Save current text state
  const handleSave = () => {
    saveMemento(mementoName, text)
  }

  // Undo the last text change
  const handleUndo = () => {
    const previousState = undoMemento(mementoName);
    if (previousState !== null) {
      setText(previousState)
    }
  }

  // Redo the last undone text change
  const handleRedo = () => {
    const nextState = redoMemento(mementoName)
    if (nextState !== null) {
      setText(nextState)
    }
  }

  // Get the current state of the text area
  const getCurrentState = () => {
    const currentState = currentMementoState(mementoName)
    if (currentState !== null) {
      setText(currentState)
    }
  }

  // Handle changes in the textarea
  const handleChange = (event) => {
    setText(event.target.value)
  }

  return (
    <div>
      <h2>Text Area with Undo/Redo</h2>
      <textarea 
        value={text}
        onChange={handleChange}
        rows="10"
        cols="50"
        placeholder="Start typing..."
      ></textarea>

      <div>
        <button onClick={handleSave}>Save State</button>
        <button onClick={handleUndo}>Undo</button>
        <button onClick={handleRedo}>Redo</button>
        <button onClick={getCurrentState}>Get Current State</button>
      </div>
    </div>
  )
}

export default TextAreaWithMemento;
```
### How It Works:
1. Save: When the user clicks "Save State", the current text in the textarea is saved into the memento manager, allowing for future state retrieval.
2. Undo: Clicking "Undo" will restore the previous state from the memento manager, allowing the user to revert to the last saved state.
3. Redo: If the user has undone a change, they can click "Redo" to restore the next state.
4. Get Current State: The "Get Current State" button allows you to view the current saved state of the textarea.
### Benefits of Using Memento Context:
* Global Access: The state is stored in a central context and cached globally using React Query. This means any component in the app can access and modify the saved states without needing to pass props down the component tree.
* Consistency: By leveraging React Query's cache, we ensure that the state is consistent across the app, and changes are persisted even if the page is reloaded or a component is re-rendered.
* Simplified State Management: Developers don't need to worry about managing state individually for each component. The Memento Context automatically handles state saving, undoing, and redoing, making state management much more efficient.
