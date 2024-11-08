# The Grid

<p class="lead">Problem: You've got tons of content, each needing different sized cells, and don't know how to quick and easily get it all done. Solution: The awesome XY grid!</p>

---

## Overview

The grid is built around two key elements: grid-x and cells. grid-container create a max-width and contain the grid, and cells create the final structure. Everything on your page that you don't give a specific structural style to should be within a grid-x or cell.

---

## Nesting

In the Grid you can nest cells down as far as you'd like. Just embed grid-x inside cells and go from there. Each embedded grid-x can contain up to 12 cells.

---

## How to Use

Using this framework is easy. Here's how your code will look when you use a series of `<div>` tags to create cells.

```html
<div class="grid-x">
  <div class="small-6 medium-4 large-3 cell">...</div>
  <div class="small-6 medium-8 large-9 cell">...</div>
</div>
```

<div class="grid-x display">
  <div class="small-12 large-4 cell">4</div>
  <div class="small-12 large-4 cell">4</div>
  <div class="small-12 large-4 cell">4</div>
</div>
<div class="grid-x display">
  <div class="small-12 large-3 cell">3</div>
  <div class="small-12 large-6 cell">6</div>
  <div class="small-12 large-3 cell">3</div>
</div>
<div class="grid-x display">
  <div class="small-12 large-2 cell">2</div>
  <div class="small-12 large-8 cell">8</div>
  <div class="small-12 large-2 cell">2</div>
</div>
<div class="grid-x display">
  <div class="small-12 large-3 cell">3</div>
  <div class="small-12 large-9 cell">9</div>
</div>
<div class="grid-x display">
  <div class="small-12 large-4 cell">4</div>
  <div class="small-12 large-8 cell">8</div>
</div>
<div class="grid-x display">
  <div class="small-12 large-5 cell">5</div>
  <div class="small-12 large-7 cell">7</div>
</div>
<div class="grid-x display">
  <div class="small-12 large-6 cell">6</div>
  <div class="small-12 large-6 cell">6</div>
</div>

---

## Nesting grid-x

In the Grid you can nest cells down as far as you'd like. Just embed grid-x inside cells and go from there. Each embedded grid-x can contain up to 12 cells.

```html
<div class="grid-x">
  <div class="small-8 cell">8
    <div class="grid-x">
      <div class="small-8 cell">8 Nested
        <div class="grid-x">
          <div class="small-8 cell">8 Nested Again</div>
          <div class="small-4 cell">4</div>
        </div>
      </div>
      <div class="small-4 cell">4</div>
    </div>
  </div>
  <div class="small-4 cell">4</div>
</div>
```

<div class="grid-x display">
  <div class="small-8 cell">8
    <div class="grid-x">
      <div class="small-8 cell">8 Nested
        <div class="grid-x">
          <div class="small-8 cell">8 Nested Again</div>
          <div class="small-4 cell">4</div>
        </div>
      </div>
      <div class="small-4 cell">4</div>
    </div>
  </div>
  <div class="small-4 cellgi">4</div>
</div>

---

## Small Grid

As you've probably noticed in the examples above, you have access to a small, medium, and large grid. If you know that your grid structure will be the same for small devices as it will be on large devices, just use the small grid. You can override your small grid classes by adding medium or large grid classes.

```html
<div class="grid-x">
  <div class="small-2 cell">2</div>
  <div class="small-10 cell">10, last</div>
</div>
<div class="grid-x">
  <div class="small-3 cell">3</div>
  <div class="small-9 cell">9, last</div>
</div>
```

<div class="grid-x display">
  <div class="small-2 cell">2</div>
  <div class="small-10 cell">10, last</div>
</div>
<div class="grid-x display">
  <div class="small-3 cell">3</div>
  <div class="small-9 cell">9, last</div>
</div>



# Colors

<p class="lead">Below you can find the different values we created that support the primary color variable you can change at any time in <code>\_settings.scss</code></p>

---

<div class="row up-1 medium-up-3 large-up-5">
  <div class="column">
    <div class="color-block">
      <span style="background: #284a8a"></span>
      Primary #284a8a
    </div>
  </div>
  <div class="column">
    <div class="color-block">
      <span style="background: #31c5f4"></span>
      Secondary #31c5f4
    </div>
  </div>
  <div class="column">
    <div class="color-block">
      <span style="background: #7eda08"></span>
      Success #7eda08
    </div>
  </div>
  <div class="column">
    <div class="color-block">
      <span style="background: #e9db00"></span>
      Warning #e9db00
    </div>
  </div>
  <div class="column">
    <div class="color-block">
      <span style="background: #ec5840"></span>
      Alert #ec5840
    </div>
  </div>
  <div class="column">
    <div class="color-block">
      <span style="background: #393939"></span>
      #393939
    </div>
  </div>
</div>



# Typography

<p class="lead">This design uses Helvetica Neue for headings and paragraph text.</p>

---

## Headings

Headings are used to denote different sections of content, usually consisting of related paragraphs and other HTML elements. They range from h1 to h6 and should be styled in a clear hierarchy (i.e., largest to smallest)

---

## Paragraphs

Paragraphs are groups of sentences, each with a lead (first sentence) and transition (last sentence). They are block level elements, meaning they stack vertically when repeated. Use them as such.

---

<h1>Heading Level 1</h1>

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Hic quibusdam ratione sunt dolorum, qui illo maxime doloremque accusantium cum libero eum, a optio odio placeat debitis ullam aut non distinctio.

<h2>Heading Level 2</h2>

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Hic quibusdam ratione sunt dolorum, qui illo maxime doloremque accusantium cum libero eum, a optio odio placeat debitis ullam aut non distinctio.

<h3>Heading Level 3</h3>

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Hic quibusdam ratione sunt dolorum, qui illo maxime doloremque accusantium cum libero eum, a optio odio placeat debitis ullam aut non distinctio.

<h4>Heading Level 4</h4>

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Hic quibusdam ratione sunt dolorum, qui illo maxime doloremque accusantium cum libero eum, a optio odio placeat debitis ullam aut non distinctio.

<h5>Heading Level 5</h5>

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Hic quibusdam ratione sunt dolorum, qui illo maxime doloremque accusantium cum libero eum, a optio odio placeat debitis ullam aut non distinctio.

<h6>Heading Level 6</h6>

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Hic quibusdam ratione sunt dolorum, qui illo maxime doloremque accusantium cum libero eum, a optio odio placeat debitis ullam aut non distinctio.



# Buttons

<p class="lead">Buttons are tied to an action of some kind, whether that button is on a cheese dispenser or launches the rocket that you're strapped to. On the web, we follow similar conventions.</p>

---

## Primary Buttons

These buttons are primary calls to action and should be used sparingly. Their size can be adjusted with the `.tiny`, `.small`, and `.large` classes.

```html_example
<a href="#" class="primary large button">Large button</a>
<a href="#" class="primary button">Regular button</a>
<a href="#" class="primary small button">Small button</a>
<a href="#" class="primary tiny button">Tiny button</a>
```

---

## Secondary Buttons

These buttons are used for less important, secondary actions on a page.

```html_example
<a href="#" class="secondary large button">Large button</a>
<a href="#" class="secondary button">Regular button</a>
<a href="#" class="secondary small button">Small button</a>
<a href="#" class="secondary tiny button">Tiny button</a>
```

---

## Light Buttons

These buttons are used on dark backgrounds.

```html_example
<a href="#" class="lightbutton large button">Large button</a>
<a href="#" class="lightbutton button">Regular button</a>
<a href="#" class="lightbutton small button">Small button</a>
<a href="#" class="lightbutton tiny button">Tiny button</a>
```



# Forms

<p class="lead">Use forms to allow users to interact with the site and provide information to the company.</p>

---

## Elements of a Form

A form should be marked up using its default HTML properties. The ones we make use of include (in hierarchical order):

- Form
- Label
- Input
- Select
- Text area
- Button

---

## How to Use

Make forms great and easy to use with the following rules:

- Wrap checkboxes and radio buttons within labels for larger hit areas, and be sure to set the for, name, and id attributes for all applicable elements.
- Series of checkboxes and radio buttons below within a `<ul class="inline-list">`.
- Before selecting any set of fields to use for a required input, explore other options (e.g., radio buttons over select lists).

---

## Learn All About Forms

Check out the [Foundation Docs](http://foundation.zurb.com/sites/docs) to learn about how flexible our forms are for creating different layouts. It works perfectly with the grid to meet all your form needs.

---

## Form Layouts

Form elements in Foundation are styled based on their type attribute rather than a class. Inputs in Foundation have another major advantage — they are full width by default. That means that inputs will run as wide as the column that contains them. However, you have two options which make these forms extremely versatile:

- You can size inputs using column sizes, like `.medium-6`, `.small-6`.
- You can create row elements inside your form and use columns for the form, including inputs, labels and more. Rows inside a form inherit some special padding to even up input spacing.

---

## Form Example

```html_example
<form>
  <div class="row">
    <div class="large-12 columns">
      <label>Label</label>
      <input type="text" placeholder="placeholder">
    </div>
  </div>
  <div class="row">
    <div class="large-6 columns">
      <label>Label</label>
      <input type="text" placeholder="placeholder">
    </div>
    <div class="large-6 columns">
      <div class="row collapse">
        <label>Label</label>
        <div class="input-group">
          <input class="input-group-field" type="text" placeholder="placeholder">
          <span class="input-group-label">.com</span>
        </div>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="large-12 columns">
      <label>Select Box</label>
      <select>
        <option value="good">Good</option>
        <option value="better">Better</option>
        <option value="best">Best</option>
      </select>
    </div>
  </div>
  <div class="row">
    <div class="large-6 columns">
      <label>Choose Your Favorite</label>
      <input type="radio" name="radio1" value="radio1" id="radio1"><label for="radio1">Red</label>
      <input type="radio" name="radio2" value="radio2" id="radio2"><label for="radio2">Blue</label>
    </div>
    <div class="large-6 columns">
      <label>Check these out</label>
      <input id="checkbox1" type="checkbox"><label for="checkbox1">Checkbox 1</label>
      <input id="checkbox2" type="checkbox"><label for="checkbox2">Checkbox 2</label>
    </div>
  </div>
  <div class="row">
    <div class="large-12 columns">
      <label>Textarea Label</label>
      <textarea placeholder="placeholder"></textarea>
    </div>
  </div>
</form>
```



# Tables

These are the table layouts for the system. Below we have the 3 main table layouts.

## Main Table

```html

<!-- Mobile Card -->
<div class="mro-main-table-card hide-for-large">
  <div class="grid-x mro-main-table-row  mro-main-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>WO # </strong>100050</p>
    </div>
    <div class="cell small-6 mro-rank">
      <p>Rank: <strong>N/A</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-main-table-row  mro-main-table-row-2">
    <div class="cell small-12 mro-needdate">
      <p>Need Date: <span>09 / 15 / 19</span> <strong>416 days</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-main-table-row  mro-main-table-row-3">
    <div class="cell small-6">
      <h3>Part Information</h3>
    </div>
    <div class="cell small-6 mro-wotype">
      <p>WO Type: <strong>N/A</strong></p>
    </div>
    <div class="cell small-6 mro-partname">
      <h2># 01 FAN (CF6-50)</h2>
    </div>
    <div class="cell small-6 mro-serialnum">
      <p>Serial #: <strong>QC ESN</strong></p>
    </div>
    <div class="cell small-12 mro-partdescrip">
      <p>Exploded View CF6 Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed adiam nonumy.</p>
    </div>
  </div>
    <ul class="accordion" data-accordion data-allow-all-closed="true">
      <li class="accordion-item" data-accordion-item>
        <a href="#deeplink1" class="accordion-title"><p>Expand More Information</p></a>
        <div class="accordion-content" data-tab-content>
          <div class="grid-x  mro-main-table-row  mro-main-table-row-4">
            <div class="cell small-12 mro-status">
              <a class="mro-status-bubble mro-status-pending" href="#">Pending</a>
              <hr/>
            </div>
            <div class="cell small-4 mro-location">
              <p>Location: <strong>N/A</strong></p>
            </div>
            <div class="cell small-8 mro-entrydate">
              <p>Entry Date: <strong>08 / 15 / 2018</strong></p>
            </div>
            <div class="cell small-6 mro-clientname">
              <p>ABC Areospace Inc.</p>
            </div>
            <div class="cell small-6 mro-customerref">
              <p>Cust Ref#: <strong>12345</strong></p>
            </div>
            <div class="cell small-6 mro-manager">
              <p>Manager: <strong>N/A</strong></p>
            </div>
            <div class="cell small-6 mro-time">
              <p>Time: <strong>N/A</strong></p>
            </div>
            <div class="cell small-12 mro-timeto-wrap">
              <p class="mro-timeto">Time: <span><strong id="mro-timeto-d">447</strong> d,</span> <span><strong id="mro-timeto-h">6</strong> h,</span> <span><strong id="mro-timeto-m">47</strong> m,</span> <span><strong id="mro-timeto-s">45</strong> s</span></p>
            </div>
          </div>
        </div>
      </li>
    </ul>
</div>
<!-- Mobile Card - END -->


<!-- Desktop Table -->

<table class="stack mro-main-table-stack show-for-large">
  <thead>
    <tr>
      <th>WO#</th>
      <th>Status</th>
      <th>Customer Info</th>
      <th>Time</th>
      <th>Need Date</th>
      <th>Rank</th>
      <th>Part Info</th>
      <th>Serial #</th>
      <th>Manager</th>
      <th>Entry Date</th>
      <th>WO Type</th>
      <th>Location</th>
      <th>Time</th>
    </tr>
  </thead>
  <tbody>
    <!-- ROW -->
    <tr>
        <!-- WO# -->
        <td class="mro-wo">
          <a href="#">100050</a>
        </td>
        <!-- Pending -->
        <td class="mro-wo">
          <a class="mro-status-bubble mro-status-pending" href="#">Pending</a>
        </td>
        <!-- Customer # -->
        <td class="mro-clientinfo">
          <p class="mro-customerref">Cust Ref #: <strong>12345</strong></p>
          <a href="#" class="mro-clientname">
            <h3>ABC Areospace Inc.</h3>
          </a>
        </td>
        <!-- Time -->
        <td class="mro-time">-</td>
        <!-- Need Date -->
        <td class="mro-needdate">
          <p>09/15/19<br/><strong>416 days</strong></p>
        </td>
        <!-- Rank -->
        <td class="mro-rank">-</td>
        <!-- Part Info -->
        <td class="mro-partname">
          <p><i># 01 FAN (CF6-50)</i><br/>Module</p>
        </td>
        <!-- Serial # -->
        <td class="mro-serialnum">
          <p>QC ESN</p>
        </td>
        <!-- Manager -->
        <td class="mro-manager">
          <p>N/A</p>
        </td>
        <!-- Entry Date -->
        <td class="mro-entrydate">
          <p>08/15/18</p>
        </td>
        <!-- WO Type -->
        <td class="mro-wotype">
          <p>N/A</p>
        </td>
        <!-- Location -->
        <td class="mro-location">
          <p>N/A</p>
        </td>
        <!-- Time -->
        <td class="mro-timeto-wrap">
          <p class="mro-timeto">Time: <span><strong id="mro-timeto-d">447</strong>d,</span> <span><strong id="mro-timeto-h">6</strong>h,</span><br/><span><strong id="mro-timeto-m">47</strong>m,</span> <span><strong id="mro-timeto-s">45</strong>s</span></p>
        </td>
    </tr>
    <!-- ROW - END -->
  </tbody>
</table>

<!-- Desktop Table - END -->

```

<!-- Mobile Card -->
<div class="mro-main-table-card hide-for-large">
  <div class="grid-x mro-main-table-row  mro-main-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>WO # </strong>100050</p>
    </div>
    <div class="cell small-6 mro-rank">
      <p>Rank: <strong>N/A</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-main-table-row  mro-main-table-row-2">
    <div class="cell small-12 mro-needdate">
      <p>Need Date: <span>09 / 15 / 19</span> <strong>416 days</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-main-table-row  mro-main-table-row-3">
    <div class="cell small-6">
      <h3>Part Information</h3>
    </div>
    <div class="cell small-6 mro-wotype">
      <p>WO Type: <strong>N/A</strong></p>
    </div>
    <div class="cell small-6 mro-partname">
      <h2># 01 FAN (CF6-50)</h2>
    </div>
    <div class="cell small-6 mro-serialnum">
      <p>Serial #: <strong>QC ESN</strong></p>
    </div>
    <div class="cell small-12 mro-partdescrip">
      <p>Exploded View CF6 Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed adiam nonumy.</p>
    </div>
  </div>
    <ul class="accordion" data-accordion data-allow-all-closed="true">
      <li class="accordion-item" data-accordion-item>
        <a href="#deeplink1" class="accordion-title"><p>Expand More Information</p></a>
        <div class="accordion-content" data-tab-content>
          <div class="grid-x  mro-main-table-row  mro-main-table-row-4">
            <div class="cell small-12 mro-status">
              <a class="mro-status-bubble mro-status-pending" href="#">Pending</a>
              <hr/>
            </div>
            <div class="cell small-4 mro-location">
              <p>Location: <strong>N/A</strong></p>
            </div>
            <div class="cell small-8 mro-entrydate">
              <p>Entry Date: <strong>08 / 15 / 2018</strong></p>
            </div>
            <div class="cell small-6 mro-clientname">
              <p>ABC Areospace Inc.</p>
            </div>
            <div class="cell small-6 mro-customerref">
              <p>Cust Ref#: <strong>12345</strong></p>
            </div>
            <div class="cell small-6 mro-manager">
              <p>Manager: <strong>N/A</strong></p>
            </div>
            <div class="cell small-6 mro-time">
              <p>Time: <strong>N/A</strong></p>
            </div>
            <div class="cell small-12 mro-timeto-wrap">
              <p class="mro-timeto">Time: <span><strong id="mro-timeto-d">447</strong> d,</span> <span><strong id="mro-timeto-h">6</strong> h,</span> <span><strong id="mro-timeto-m">47</strong> m,</span> <span><strong id="mro-timeto-s">45</strong> s</span></p>
            </div>
          </div>
        </div>
      </li>
    </ul>
</div>
<!-- Mobile Card - END -->

<!-- Mobile Card -->
<div class="mro-main-table-card hide-for-large">
  <div class="grid-x mro-main-table-row  mro-main-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>WO # </strong>100050</p>
    </div>
    <div class="cell small-6 mro-rank">
      <p>Rank: <strong>N/A</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-main-table-row  mro-main-table-row-2">
    <div class="cell small-12 mro-needdate">
      <p>Need Date: <span>09 / 15 / 19</span> <strong>416 days</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-main-table-row  mro-main-table-row-3">
    <div class="cell small-6">
      <h3>Part Information</h3>
    </div>
    <div class="cell small-6 mro-wotype">
      <p>WO Type: <strong>N/A</strong></p>
    </div>
    <div class="cell small-6 mro-partname">
      <h2># 01 FAN (CF6-50)</h2>
    </div>
    <div class="cell small-6 mro-serialnum">
      <p>Serial #: <strong>QC ESN</strong></p>
    </div>
    <div class="cell small-12 mro-partdescrip">
      <p>Exploded View CF6 Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed adiam nonumy.</p>
    </div>
  </div>
    <ul class="accordion" data-accordion data-allow-all-closed="true">
      <li class="accordion-item" data-accordion-item>
        <a href="#deeplink1" class="accordion-title"><p>Expand More Information</p></a>
        <div class="accordion-content" data-tab-content>
          <div class="grid-x  mro-main-table-row  mro-main-table-row-4">
            <div class="cell small-12 mro-status">
              <a class="mro-status-bubble mro-status-done" href="#">Done</a>
              <hr/>
            </div>
            <div class="cell small-4 mro-location">
              <p>Location: <strong>N/A</strong></p>
            </div>
            <div class="cell small-8 mro-entrydate">
              <p>Entry Date: <strong>08 / 15 / 2018</strong></p>
            </div>
            <div class="cell small-6 mro-clientname">
              <p>ABC Areospace Inc.</p>
            </div>
            <div class="cell small-6 mro-customerref">
              <p>Cust Ref#: <strong>12345</strong></p>
            </div>
            <div class="cell small-6 mro-manager">
              <p>Manager: <strong>N/A</strong></p>
            </div>
            <div class="cell small-6 mro-time">
              <p>Time: <strong>N/A</strong></p>
            </div>
            <div class="cell small-12 mro-timeto-wrap">
              <p class="mro-timeto">Time: <span><strong id="mro-timeto-d">447</strong> d,</span> <span><strong id="mro-timeto-h">6</strong> h,</span> <span><strong id="mro-timeto-m">47</strong> m,</span> <span><strong id="mro-timeto-s">45</strong> s</span></p>
            </div>
          </div>
        </div>
      </li>
    </ul>
</div>
<!-- Mobile Card - END -->

<!-- Mobile Card -->
<div class="mro-main-table-card hide-for-large">
  <div class="grid-x mro-main-table-row  mro-main-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>WO # </strong>100050</p>
    </div>
    <div class="cell small-6 mro-rank">
      <p>Rank: <strong>N/A</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-main-table-row  mro-main-table-row-2">
    <div class="cell small-12 mro-needdate">
      <p>Need Date: <span>09 / 15 / 19</span> <strong>416 days</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-main-table-row  mro-main-table-row-3">
    <div class="cell small-6">
      <h3>Part Information</h3>
    </div>
    <div class="cell small-6 mro-wotype">
      <p>WO Type: <strong>N/A</strong></p>
    </div>
    <div class="cell small-6 mro-partname">
      <h2># 01 FAN (CF6-50)</h2>
    </div>
    <div class="cell small-6 mro-serialnum">
      <p>Serial #: <strong>QC ESN</strong></p>
    </div>
    <div class="cell small-12 mro-partdescrip">
      <p>Exploded View CF6 Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed adiam nonumy.</p>
    </div>
  </div>
    <ul class="accordion" data-accordion data-allow-all-closed="true">
      <li class="accordion-item" data-accordion-item>
        <a href="#deeplink1" class="accordion-title"><p>Expand More Information</p></a>
        <div class="accordion-content" data-tab-content>
          <div class="grid-x  mro-main-table-row  mro-main-table-row-4">
            <div class="cell small-12 mro-status">
              <a class="mro-status-bubble mro-status-done" href="#">Done</a>
              <hr/>
            </div>
            <div class="cell small-4 mro-location">
              <p>Location: <strong>N/A</strong></p>
            </div>
            <div class="cell small-8 mro-entrydate">
              <p>Entry Date: <strong>08 / 15 / 2018</strong></p>
            </div>
            <div class="cell small-6 mro-clientname">
              <p>ABC Areospace Inc.</p>
            </div>
            <div class="cell small-6 mro-customerref">
              <p>Cust Ref#: <strong>12345</strong></p>
            </div>
            <div class="cell small-6 mro-manager">
              <p>Manager: <strong>N/A</strong></p>
            </div>
            <div class="cell small-6 mro-time">
              <p>Time: <strong>N/A</strong></p>
            </div>
            <div class="cell small-12 mro-timeto-wrap">
              <p class="mro-timeto">Time: <span><strong id="mro-timeto-d">447</strong> d,</span> <span><strong id="mro-timeto-h">6</strong> h,</span> <span><strong id="mro-timeto-m">47</strong> m,</span> <span><strong id="mro-timeto-s">45</strong> s</span></p>
            </div>
          </div>
        </div>
      </li>
    </ul>
</div>
<!-- Mobile Card - END -->

<!-- Desktop Table -->

<table class="stack mro-main-table-stack show-for-large">
  <thead>
    <tr>
      <th>WO#</th>
      <th>Status</th>
      <th>Customer Info</th>
      <th>Time</th>
      <th>Need Date</th>
      <th>Rank</th>
      <th>Part Info</th>
      <th>Serial #</th>
      <th>Manager</th>
      <th>Entry Date</th>
      <th>WO Type</th>
      <th>Location</th>
      <th>Time</th>
    </tr>
  </thead>
  <tbody>
    <!-- ROW -->
    <tr>
        <!-- WO# -->
        <td class="mro-wo">
          <a href="#">100050</a>
        </td>
        <!-- Pending -->
        <td class="mro-wo">
          <a class="mro-status-bubble mro-status-pending" href="#">Pending</a>
        </td>
        <!-- Customer # -->
        <td class="mro-clientinfo">
          <p class="mro-customerref">Cust Ref #: <strong>12345</strong></p>
          <a href="#" class="mro-clientname">
            <h3>ABC Areospace Inc.</h3>
          </a>
        </td>
        <!-- Time -->
        <td class="mro-time">-</td>
        <!-- Need Date -->
        <td class="mro-needdate">
          <p>09/15/19<br/><strong>416 days</strong></p>
        </td>
        <!-- Rank -->
        <td class="mro-rank">-</td>
        <!-- Part Info -->
        <td class="mro-partname">
          <p><i># 01 FAN (CF6-50)</i><br/>Module</p>
        </td>
        <!-- Serial # -->
        <td class="mro-serialnum">
          <p>QC ESN</p>
        </td>
        <!-- Manager -->
        <td class="mro-manager">
          <p>N/A</p>
        </td>
        <!-- Entry Date -->
        <td class="mro-entrydate">
          <p>08/15/18</p>
        </td>
        <!-- WO Type -->
        <td class="mro-wotype">
          <p>N/A</p>
        </td>
        <!-- Location -->
        <td class="mro-location">
          <p>N/A</p>
        </td>
        <!-- Time -->
        <td class="mro-timeto-wrap">
          <p class="mro-timeto">Time: <span><strong id="mro-timeto-d">447</strong>d,</span> <span><strong id="mro-timeto-h">6</strong>h,</span><br/><span><strong id="mro-timeto-m">47</strong>m,</span> <span><strong id="mro-timeto-s">45</strong>s</span></p>
        </td>
    </tr>
    <!-- ROW - END -->
    <!-- ROW -->
    <tr>
        <!-- WO# -->
        <td class="mro-wo">
          <a href="#">100050</a>
        </td>
        <!-- Pending -->
        <td class="mro-wo">
          <a class="mro-status-bubble mro-status-done" href="#">Done</a>
        </td>
        <!-- Customer # -->
        <td class="mro-clientinfo">
          <p class="mro-customerref">Cust Ref #: <strong>12345</strong></p>
          <a href="#" class="mro-clientname">
            <h3>ABC Areospace Inc.</h3>
          </a>
        </td>
        <!-- Time -->
        <td class="mro-time">-</td>
        <!-- Need Date -->
        <td class="mro-needdate">
          <p>09/15/19<br/><strong>416 days</strong></p>
        </td>
        <!-- Rank -->
        <td class="mro-rank">-</td>
        <!-- Part Info -->
        <td class="mro-partname">
          <p><i># 01 FAN (CF6-50)</i><br/>Module</p>
        </td>
        <!-- Serial # -->
        <td class="mro-serialnum">
          <p>QC ESN</p>
        </td>
        <!-- Manager -->
        <td class="mro-manager">
          <p>N/A</p>
        </td>
        <!-- Entry Date -->
        <td class="mro-entrydate">
          <p>08/15/18</p>
        </td>
        <!-- WO Type -->
        <td class="mro-wotype">
          <p>N/A</p>
        </td>
        <!-- Location -->
        <td class="mro-location">
          <p>N/A</p>
        </td>
        <!-- Time -->
        <td class="mro-timeto-wrap">
          <p class="mro-timeto">Time: <span><strong id="mro-timeto-d">447</strong>d,</span> <span><strong id="mro-timeto-h">6</strong>h,</span><br/><span><strong id="mro-timeto-m">47</strong>m,</span> <span><strong id="mro-timeto-s">45</strong>s</span></p>
        </td>
    </tr>
    <!-- ROW - END -->
    <!-- ROW -->
    <tr>
        <!-- WO# -->
        <td class="mro-wo">
          <a href="#">100050</a>
        </td>
        <!-- Pending -->
        <td class="mro-wo">
          <a class="mro-status-bubble mro-status-done" href="#">Done</a>
        </td>
        <!-- Customer # -->
        <td class="mro-clientinfo">
          <p class="mro-customerref">Cust Ref #: <strong>12345</strong></p>
          <a href="#" class="mro-clientname">
            <h3>ABC Areospace Inc.</h3>
          </a>
        </td>
        <!-- Time -->
        <td class="mro-time">-</td>
        <!-- Need Date -->
        <td class="mro-needdate">
          <p>09/15/19<br/><strong>416 days</strong></p>
        </td>
        <!-- Rank -->
        <td class="mro-rank">-</td>
        <!-- Part Info -->
        <td class="mro-partname">
          <p><i># 01 FAN (CF6-50)</i><br/>Module</p>
        </td>
        <!-- Serial # -->
        <td class="mro-serialnum">
          <p>QC ESN</p>
        </td>
        <!-- Manager -->
        <td class="mro-manager">
          <p>N/A</p>
        </td>
        <!-- Entry Date -->
        <td class="mro-entrydate">
          <p>08/15/18</p>
        </td>
        <!-- WO Type -->
        <td class="mro-wotype">
          <p>N/A</p>
        </td>
        <!-- Location -->
        <td class="mro-location">
          <p>N/A</p>
        </td>
        <!-- Time -->
        <td class="mro-timeto-wrap">
          <p class="mro-timeto">Time: <span><strong id="mro-timeto-d">447</strong>d,</span> <span><strong id="mro-timeto-h">6</strong>h,</span><br/><span><strong id="mro-timeto-m">47</strong>m,</span> <span><strong id="mro-timeto-s">45</strong>s</span></p>
        </td>
    </tr>
    <!-- ROW - END -->


  </tbody>
</table>

<!-- Desktop Table - END -->

---

## Barcoding Table

```html

<!-- Mobile Card -->
<div class="mro-barcoding-table-card hide-for-large">
  <div class="grid-x mro-barcoding-table-row  mro-barcoding-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>WO # </strong>100050</p>
    </div>
    <div class="cell small-6 mro-serial">
      <p>Serial #: <strong>4893</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-2">
    <div class="cell small-12 mro-partinfo">
      <div class="cell small-12 mro-partname">
        <p>Part #: <strong>28B14-17C</strong></p>
      </div>
      <div class="cell small-12 mro-partdescrip">
        <p>Exploded View CF6 Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed adiam nonumy.</p>
      </div>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-3">
    <div class="cell small-3">
      <p>Ctrl <strong>(1,))</strong></p>
    </div>
    <div class="cell small-4">
      <p>Ctrl ID <strong>(2242)</strong></p>
    </div>
    <div class="cell small-5 mro-rack">
      <p>Rack <strong>('CART 01'.)</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-4">
    <div class="cell small-7 mro-warehouse">
      <p>Warehouse: <strong>Florida</strong></p>
    </div>
    <div class="cell small-5 mro-location">
      <p>Location: <strong>F6879</strong></p>
    </div>
  </div>
</div>
<!-- Mobile Card - END -->


<!-- Desktop Table -->

<table class="stack mro-barcoding-table-stack show-for-large">
  <thead>
    <tr>
      <th>WO#</th>
      <th>Part #</th>
      <th>Description</th>
      <th>Serial #</th>
      <th>Ctrl #</th>
      <th>Ctrl ID</th>
      <th>Warehouse</th>
      <th>Location</th>
      <th>Rack</th>
    </tr>
  </thead>
  <tbody>
    <!-- ROW -->
    <tr>
        <!-- WO# -->
        <td class="mro-wo">
          <a href="#"><p>100050</p></a>
        </td>
        <!-- Part Number -->
        <td class="mro-partnum">
          <a href="#"><p>28B141-17C</p></a>
        </td>
        <!-- Description -->
        <td class="mro-descrip">
          <p>Generator, Alternating Current Lorem Ipsum dolor sit armet, consetetur sadipscing elitr.</p>
        </td>
        <!-- Serial # -->
        <td class="mro-serialnum"><p><strong># 4893</strong></p></td>
        <!-- Ctrl # -->
        <td class="mro-ctrlnum">
          <p>(1,)</p>
        </td>
        <!-- Ctrl ID -->
        <td class="mro-ctrlid"><p>(2242)</p></td>
        <!-- Waregouse -->
        <td class="mro-warehouse">
          <p>Florida</p>
        </td>
        <!-- Location -->
        <td class="mro-location">
          <p>N/A</p>
        </td>
        <!-- Rack -->
        <td class="mro-Rack">
          <p><strong>('CART 01',)</strong></p>
        </td>
    </tr>
    <!-- ROW - END -->
  </tbody>
</table>

<!-- Desktop Table - END -->

```

<!-- Mobile Card -->
<div class="mro-barcoding-table-card hide-for-large">
  <div class="grid-x mro-barcoding-table-row  mro-barcoding-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>WO # </strong>100050</p>
    </div>
    <div class="cell small-6 mro-serial">
      <p>Serial #: <strong>4893</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-2">
    <div class="cell small-12 mro-partinfo">
      <div class="cell small-12 mro-partname">
        <p>Part #: <strong>28B14-17C</strong></p>
      </div>
      <div class="cell small-12 mro-partdescrip">
        <p>Exploded View CF6 Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed adiam nonumy.</p>
      </div>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-3">
    <div class="cell small-3">
      <p>Ctrl <strong>(1,))</strong></p>
    </div>
    <div class="cell small-4">
      <p>Ctrl ID <strong>(2242)</strong></p>
    </div>
    <div class="cell small-5 mro-rack">
      <p>Rack <strong>('CART 01'.)</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-4">
    <div class="cell small-7 mro-warehouse">
      <p>Warehouse: <strong>Florida</strong></p>
    </div>
    <div class="cell small-5 mro-location">
      <p>Location: <strong>F6879</strong></p>
    </div>
  </div>
</div>
<!-- Mobile Card - END -->
<!-- Mobile Card -->
<div class="mro-barcoding-table-card hide-for-large">
  <div class="grid-x mro-barcoding-table-row  mro-barcoding-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>WO # </strong>100050</p>
    </div>
    <div class="cell small-6 mro-serial">
      <p>Serial #: <strong>4893</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-2">
    <div class="cell small-12 mro-partinfo">
      <div class="cell small-12 mro-partname">
        <p>Part #: <strong>28B14-17C</strong></p>
      </div>
      <div class="cell small-12 mro-partdescrip">
        <p>Exploded View CF6 Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed adiam nonumy.</p>
      </div>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-3">
    <div class="cell small-3">
      <p>Ctrl <strong>(1,))</strong></p>
    </div>
    <div class="cell small-4">
      <p>Ctrl ID <strong>(2242)</strong></p>
    </div>
    <div class="cell small-5 mro-rack">
      <p>Rack <strong>('CART 01'.)</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-4">
    <div class="cell small-7 mro-warehouse">
      <p>Warehouse: <strong>Florida</strong></p>
    </div>
    <div class="cell small-5 mro-location">
      <p>Location: <strong>F6879</strong></p>
    </div>
  </div>
</div>
<!-- Mobile Card - END -->
<!-- Mobile Card -->
<div class="mro-barcoding-table-card hide-for-large">
  <div class="grid-x mro-barcoding-table-row  mro-barcoding-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>WO # </strong>100050</p>
    </div>
    <div class="cell small-6 mro-serial">
      <p>Serial #: <strong>4893</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-2">
    <div class="cell small-12 mro-partinfo">
      <div class="cell small-12 mro-partname">
        <p>Part #: <strong>28B14-17C</strong></p>
      </div>
      <div class="cell small-12 mro-partdescrip">
        <p>Exploded View CF6 Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed adiam nonumy.</p>
      </div>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-3">
    <div class="cell small-3">
      <p>Ctrl <strong>(1,))</strong></p>
    </div>
    <div class="cell small-4">
      <p>Ctrl ID <strong>(2242)</strong></p>
    </div>
    <div class="cell small-5 mro-rack">
      <p>Rack <strong>('CART 01'.)</strong></p>
    </div>
  </div>
  <div class="grid-x  mro-barcoding-table-row  mro-barcoding-table-row-4">
    <div class="cell small-7 mro-warehouse">
      <p>Warehouse: <strong>Florida</strong></p>
    </div>
    <div class="cell small-5 mro-location">
      <p>Location: <strong>F6879</strong></p>
    </div>
  </div>
</div>
<!-- Mobile Card - END -->

<!-- Desktop Table -->

<table class="stack mro-barcoding-table-stack show-for-large">
  <thead>
    <tr>
      <th>WO#</th>
      <th>Part #</th>
      <th>Description</th>
      <th>Serial #</th>
      <th>Ctrl #</th>
      <th>Ctrl ID</th>
      <th>Warehouse</th>
      <th>Location</th>
      <th>Rack</th>
    </tr>
  </thead>
  <tbody>
    <!-- ROW -->
    <tr>
        <!-- WO# -->
        <td class="mro-wo">
          <a href="#"><p>100050</p></a>
        </td>
        <!-- Part Number -->
        <td class="mro-partnum">
          <a href="#"><p>28B141-17C</p></a>
        </td>
        <!-- Description -->
        <td class="mro-descrip">
          <p>Generator, Alternating Current Lorem Ipsum dolor sit armet, consetetur sadipscing elitr.</p>
        </td>
        <!-- Serial # -->
        <td class="mro-serialnum"><p><strong># 4893</strong></p></td>
        <!-- Ctrl # -->
        <td class="mro-ctrlnum">
          <p>(1,)</p>
        </td>
        <!-- Ctrl ID -->
        <td class="mro-ctrlid"><p>(2242)</p></td>
        <!-- Waregouse -->
        <td class="mro-warehouse">
          <p>Florida</p>
        </td>
        <!-- Location -->
        <td class="mro-location">
          <p>N/A</p>
        </td>
        <!-- Rack -->
        <td class="mro-Rack">
          <p><strong>('CART 01',)</strong></p>
        </td>
    </tr>
    <!-- ROW - END -->
    <!-- ROW -->
    <tr>
        <!-- WO# -->
        <td class="mro-wo">
          <a href="#"><p>100050</p></a>
        </td>
        <!-- Part Number -->
        <td class="mro-partnum">
          <a href="#"><p>28B141-17C</p></a>
        </td>
        <!-- Description -->
        <td class="mro-descrip">
          <p>Generator, Alternating Current Lorem Ipsum dolor sit armet, consetetur sadipscing elitr.</p>
        </td>
        <!-- Serial # -->
        <td class="mro-serialnum"><p><strong># 4893</strong></p></td>
        <!-- Ctrl # -->
        <td class="mro-ctrlnum">
          <p>(1,)</p>
        </td>
        <!-- Ctrl ID -->
        <td class="mro-ctrlid"><p>(2242)</p></td>
        <!-- Waregouse -->
        <td class="mro-warehouse">
          <p>Florida</p>
        </td>
        <!-- Location -->
        <td class="mro-location">
          <p>N/A</p>
        </td>
        <!-- Rack -->
        <td class="mro-Rack">
          <p><strong>('CART 01',)</strong></p>
        </td>
    </tr>
    <!-- ROW - END -->
    <!-- ROW -->
    <tr>
        <!-- WO# -->
        <td class="mro-wo">
          <a href="#"><p>100050</p></a>
        </td>
        <!-- Part Number -->
        <td class="mro-partnum">
          <a href="#"><p>28B141-17C</p></a>
        </td>
        <!-- Description -->
        <td class="mro-descrip">
          <p>Generator, Alternating Current Lorem Ipsum dolor sit armet, consetetur sadipscing elitr.</p>
        </td>
        <!-- Serial # -->
        <td class="mro-serialnum"><p><strong># 4893</strong></p></td>
        <!-- Ctrl # -->
        <td class="mro-ctrlnum">
          <p>(1,)</p>
        </td>
        <!-- Ctrl ID -->
        <td class="mro-ctrlid"><p>(2242)</p></td>
        <!-- Waregouse -->
        <td class="mro-warehouse">
          <p>Florida</p>
        </td>
        <!-- Location -->
        <td class="mro-location">
          <p>N/A</p>
        </td>
        <!-- Rack -->
        <td class="mro-Rack">
          <p><strong>('CART 01',)</strong></p>
        </td>
    </tr>
    <!-- ROW - END -->
  </tbody>
</table>

<!-- Desktop Table - END -->

---

## Physical Inventory Table


```html

<!-- Mobile Card -->
<div class="mro-physical-table-card hide-for-large">
  <div class="grid-x mro-physical-table-row  mro-physical-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>User </strong>N/A</p>
    </div>
    <div class="cell small-6 mro-serial">
      <p>Batch #: <strong>30001</strong></p>
    </div>
  </div>
  <div class="grid-x mro-physical-table-row  mro-physical-table-row-2">
    <div class="cell small-12 mro-location">
      <p>Location</p>
      <h3>R19020</h3>
    </div>
  </div>
  <div class="grid-x  mro-physical-table-row  mro-physical-table-row-3">
    <div class="cell small-4">
      <p>Ctrl # <strong>1078</strong></p>
    </div>
    <div class="cell small-4">
      <p>Ctrl ID <strong>1</strong></p>
    </div>
    <div class="cell small-4 mro-rack">
      <p>Quantity <strong>1.0</strong></p>
    </div>
  </div>
</div>
<!-- Mobile Card - END -->


<!-- Desktop Table -->

<table class="stack mro-physical-table-stack show-for-large">
  <thead>
    <tr>
      <th>User</th>
      <th>Batch Number</th>
      <th>Quantity</th>
      <th>Ctrl #</th>
      <th>Ctrl ID</th>
      <th>Location</th>
    </tr>
  </thead>
  <tbody>
    <!-- ROW -->
    <tr>
        <!-- User -->
        <td class="mro-user">
          <a href="#">N/A</a>
        </td>
        <!-- Batch Number -->
        <td class="mro-Batch">
          <p><strong># 30001</strong></p>
        </td>
        <!-- Quantity -->
        <td class="mro-quanitity">
          <p>1.0</p>
        </td>
        <!-- Ctrl # -->
        <td class="mro-ctrlnum"><p><strong>10078</strong></p></td>
        <!-- Ctrl ID -->
        <td class="mro-ctrlid">
          <p>1</p>
        </td>
        <!-- Location -->
        <td class="mro-location"><p>R19020</p></td>
    </tr>
    <!-- ROW - END -->
  </tbody>
</table>

<!-- Desktop Table - END -->

```

<!-- Mobile Card -->
<div class="mro-physical-table-card hide-for-large">
  <div class="grid-x mro-physical-table-row  mro-physical-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>User </strong>N/A</p>
    </div>
    <div class="cell small-6 mro-serial">
      <p>Batch #: <strong>30001</strong></p>
    </div>
  </div>
  <div class="grid-x mro-physical-table-row  mro-physical-table-row-2">
    <div class="cell small-12 mro-location">
      <p>Location</p>
      <h3>R19020</h3>
    </div>
  </div>
  <div class="grid-x  mro-physical-table-row  mro-physical-table-row-3">
    <div class="cell small-4">
      <p>Ctrl # <strong>1078</strong></p>
    </div>
    <div class="cell small-4">
      <p>Ctrl ID <strong>1</strong></p>
    </div>
    <div class="cell small-4 mro-rack">
      <p>Quantity <strong>1.0</strong></p>
    </div>
  </div>
</div>
<!-- Mobile Card - END -->
<!-- Mobile Card -->
<div class="mro-physical-table-card hide-for-large">
  <div class="grid-x mro-physical-table-row  mro-physical-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>User </strong>N/A</p>
    </div>
    <div class="cell small-6 mro-serial">
      <p>Batch #: <strong>30001</strong></p>
    </div>
  </div>
  <div class="grid-x mro-physical-table-row  mro-physical-table-row-2">
    <div class="cell small-12 mro-location">
      <p>Location</p>
      <h3>R19020</h3>
    </div>
  </div>
  <div class="grid-x  mro-physical-table-row  mro-physical-table-row-3">
    <div class="cell small-4">
      <p>Ctrl # <strong>1078</strong></p>
    </div>
    <div class="cell small-4">
      <p>Ctrl ID <strong>1</strong></p>
    </div>
    <div class="cell small-4 mro-rack">
      <p>Quantity <strong>1.0</strong></p>
    </div>
  </div>
</div>
<!-- Mobile Card - END -->
<!-- Mobile Card -->
<div class="mro-physical-table-card hide-for-large">
  <div class="grid-x mro-physical-table-row  mro-physical-table-row-1">
    <div class="cell small-6 mro-wo">
      <p><strong>User </strong>N/A</p>
    </div>
    <div class="cell small-6 mro-serial">
      <p>Batch #: <strong>30001</strong></p>
    </div>
  </div>
  <div class="grid-x mro-physical-table-row  mro-physical-table-row-2">
    <div class="cell small-12 mro-location">
      <p>Location</p>
      <h3>R19020</h3>
    </div>
  </div>
  <div class="grid-x  mro-physical-table-row  mro-physical-table-row-3">
    <div class="cell small-4">
      <p>Ctrl # <strong>1078</strong></p>
    </div>
    <div class="cell small-4">
      <p>Ctrl ID <strong>1</strong></p>
    </div>
    <div class="cell small-4 mro-rack">
      <p>Quantity <strong>1.0</strong></p>
    </div>
  </div>
</div>
<!-- Mobile Card - END -->

<!-- Desktop Table -->

<table class="stack mro-physical-table-stack show-for-large">
  <thead>
    <tr>
      <th>User</th>
      <th>Batch Number</th>
      <th>Quantity</th>
      <th>Ctrl #</th>
      <th>Ctrl ID</th>
      <th>Location</th>
    </tr>
  </thead>
  <tbody>
    <!-- ROW -->
    <tr>
        <!-- User -->
        <td class="mro-user">
          <a href="#">N/A</a>
        </td>
        <!-- Batch Number -->
        <td class="mro-Batch">
          <p><strong># 30001</strong></p>
        </td>
        <!-- Quantity -->
        <td class="mro-quanitity">
          <p>1.0</p>
        </td>
        <!-- Ctrl # -->
        <td class="mro-ctrlnum"><p><strong>10078</strong></p></td>
        <!-- Ctrl ID -->
        <td class="mro-ctrlid">
          <p>1</p>
        </td>
        <!-- Location -->
        <td class="mro-location"><p>R19020</p></td>
    </tr>
    <!-- ROW - END -->
    <!-- ROW -->
    <tr>
        <!-- User -->
        <td class="mro-user">
          <a href="#">N/A</a>
        </td>
        <!-- Batch Number -->
        <td class="mro-Batch">
          <p><strong># 30001</strong></p>
        </td>
        <!-- Quantity -->
        <td class="mro-quanitity">
          <p>1.0</p>
        </td>
        <!-- Ctrl # -->
        <td class="mro-ctrlnum"><p><strong>10078</strong></p></td>
        <!-- Ctrl ID -->
        <td class="mro-ctrlid">
          <p>1</p>
        </td>
        <!-- Location -->
        <td class="mro-location"><p>R19020</p></td>
    </tr>
    <!-- ROW - END -->
    <!-- ROW -->
    <tr>
        <!-- User -->
        <td class="mro-user">
          <a href="#">N/A</a>
        </td>
        <!-- Batch Number -->
        <td class="mro-Batch">
          <p><strong># 30001</strong></p>
        </td>
        <!-- Quantity -->
        <td class="mro-quanitity">
          <p>1.0</p>
        </td>
        <!-- Ctrl # -->
        <td class="mro-ctrlnum"><p><strong>10078</strong></p></td>
        <!-- Ctrl ID -->
        <td class="mro-ctrlid">
          <p>1</p>
        </td>
        <!-- Location -->
        <td class="mro-location"><p>R19020</p></td>
    </tr>
    <!-- ROW - END -->
  </tbody>
</table>

<!-- Desktop Table - END -->
