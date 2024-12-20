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
Skopiuj kod
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
