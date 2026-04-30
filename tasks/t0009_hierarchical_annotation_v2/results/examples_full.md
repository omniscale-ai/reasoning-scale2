### Example 82: WorkArena++ (pilot_row_index=84)

**task_id**: `m2w_17fffbee-e41b-46e4-ab75-675b263ca7b7`\
**judge_verdict**: `acceptable`

**Input (annotator prompt user message)**:

```text
Benchmark: WorkArena++
Domain: web agent / Digital (Mind2Web proxy — WorkArena++ unavailable on HF)

Problem:
Find the cheapest power supply unit with at least 600W power output.
```

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Search an e-commerce site for power supply units, filter by minimum 600W power output, sort by price ascending, and identify the cheapest compliant option.",
    "subtasks": [
      {
        "subtask": "Access the product search functionality and load power supply unit results",
        "atomics": [
          "Navigate to the e-commerce site homepage",
          "Locate and click the search bar or power supply category link",
          "Enter search query for 'power supply unit' or navigate to power supplies category",
          "Execute search and wait for results page to load"
        ]
      },
      {
        "subtask": "Apply power output filter to show only units with at least 600W",
        "atomics": [
          "Identify the power output/wattage filter in the sidebar or filter panel",
          "Set the minimum power threshold to 600W",
          "Click apply filter button to update results",
          "Verify results list updates to display only 600W+ products"
        ]
      },
      {
        "subtask": "Sort filtered results by price in ascending order",
        "atomics": [
          "Locate the sort dropdown or sort controls on the results page",
          "Click sort dropdown and select 'Price: Low to High' or equivalent ascending option",
          "Confirm the results re-order with cheapest items appearing first"
        ]
      },
      {
        "subtask": "Extract and verify details of the cheapest power supply unit",
        "atomics": [
          "Identify the first result in the sorted list (lowest price)",
          "Record the product name and model number",
          "Record the product price",
          "Confirm the power specification in listing meets or exceeds 600W"
        ]
      }
    ],
    "global_atomics": [
      "Verify the final answer includes product name, price, and confirmed 600W+ specification",
      "Scan remaining top results to confirm no cheaper 600W+ alternative was missed"
    ]
  },
  "gold_actions": {
    "global": "Query e-commerce platform for power supply units with \u2265600W output, sort by ascending price, and return the cheapest unit's name and price.",
    "subtasks": [
      {
        "subtask": "Navigate to and search product database for power supply units",
        "atomics": [
          "Click search bar, type 'power supply unit', press enter or click search button",
          "Or navigate via category menu to Power Supplies section",
          "Wait for
```

**Judge verdict + justification**:

`acceptable` — Global statement captures the overall plan in one sentence; subtasks cover search,
filter by 600W, sort by price, and extract details; atomics are operational steps that execute each
subtask; global_atomics contain verification steps that cross subtasks; gold_actions mirrors the
structure with specific resolved actions.

### Example 1: FrontierScience-Olympiad (pilot_row_index=1)

**task_id**: `fs_4225f097-0cee-4e43-b5b9-6efbab4c3447`\
**judge_verdict**: `acceptable`

**Input (annotator prompt user message)**:

```text
Benchmark: FrontierScience-Olympiad
Domain: physics

Problem:
A uniformly thick, disk-shaped permanent magnet has a uniform magnetization within its body, with the direction of magnetization perpendicular to the top of the disk. (The "top" is one of the two flat surfaces of the disk, not a curved side.)

The radius of the magnet is `\(2R\)`, and the thickness is `\( d \)`, with `\(d \ll R\)`. The magnetic field at the center of the magnet is `\(\vec{B}_{0}\)`.

Now, a hole of radius `\(R\) and thickness \( d \)` is hollowed out from the center of the magnet, which means that now the leftover magnet is an annular disk of thickness `\( d \)`, inner radius `\( R \)` and outer radius `\( 2R \)`. After hollowing, the magnetization vector within the magnet remains unchanged. Find an equation for the magnetic field vector `\(\vec{B}_{1}\)` at the center of the hollowed region. Express the answer in terms of `\(\vec{B}_{0}\), \( R \)` `and \( d \).`

Think step by step and solve the problem below. At the end of your response, write your final answer on a new line starting with “FINAL ANSWER”. It should be an answer to the question such as providing a number, mathematical expression, formula, or entity name, without any extra commentary or providing multiple answer attempts.
```

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Apply superposition to express the hollow disk's magnetic field as the original field minus the removed disk's field, then determine the removed disk's contribution using the scaling relationship between field and radius for magnetized disks.",
    "subtasks": [
      {
        "subtask": "Establish the superposition framework",
        "atomics": [
          "Recognize that magnetic field obeys superposition: B_total = B_outer_annulus + B_inner_disk",
          "Rewrite as B\u2081 = B\u2080 - B_removed, where B_removed is the field from the removed disk of radius R"
        ]
      },
      {
        "subtask": "Determine field scaling with disk radius",
        "atomics": [
          "Identify that the dominant field contribution arises from surface magnetization currents K_m = M \u00d7 n\u0302 on the cylindrical edges",
          "Calculate that the surface current magnitude is I = M\u00b7d, independent of radius",
          "Apply the formula for axial field from a current loop: B = (\u03bc\u2080\u00b7I)/(2a), showing B \u221d 1/a",
          "Conclude that field scales inversely with disk radius for fixed magnetization and thickness"
        ]
      },
      {
        "subtask": "Calculate field from the removed disk",
        "atomics": [
          "Apply the scaling relation: if radius 2R produces B\u2080, then radius R produces field B_R = B\u2080\u00b7(2R/R) = 2B\u2080",
          "Verify that both removed and original disks have identical magnetization M and thickness d"
        ]
      },
      {
        "subtask": "Apply superposition to find the final field",
        "atomics": [
          "Compute B\u2081 = B\u2080 - B_removed = B\u2080 - 2B\u2080",
          "Simplify to obtain B\u2081 = -B\u2080"
        ]
      }
    ],
    "global_atomics": [
      "Confirm that the field reversal is physically consistent: the inner cylindrical surface (from the hollow) produces a stronger opposing field than the outer surface",
      "Verify the result is dimensionally consistent and does not require additional dependence on R or d beyond what B\u2080 encodes"
    ]
  },
  "gold_actions": {
    "global": "Use B\u2081 = B\u2080 - B_removed where B_removed scales as 1/R for the disk of radius R, yielding B\u2081 = -B\u2080.",
    "subtasks": [
      {
        "subtask": "Apply superposition decomposition",
        "atomics": [
          "Decompose: magnetic field of annular disk = field of full disk \u2212 field of removed
```

**Judge verdict + justification**:

`acceptable` — The global statement clearly articulates the superposition strategy and scaling
relationship. The four subtasks logically progress from establishing superposition, through deriving
the 1/a scaling law, calculating the removed disk's contribution (2B₀), to obtaining B₁ = −B₀. All
atomics are operational steps that would execute this plan; global_atomics provide valid
cross-subtask verification. The gold_actions mirror this structure with resolved calculations, and
the underlying physics (superposition + edge-current dominance yielding inverse-radius scaling) is
sound.

### Example 14: FrontierScience-Olympiad (pilot_row_index=14)

**task_id**: `fs_5ef8b29d-7665-45e6-a26a-bd4a27f450ad`\
**judge_verdict**: `needs revision`

**Input (annotator prompt user message)**:

```text
Benchmark: FrontierScience-Olympiad
Domain: chemistry

Problem:
Unknown molecule X reacts with &lt;INCHI&gt;InChI=1S/C7H8O3S/c1-6-2-4-7(5-3-6)11(8,9)10/h2-5H,1H3,(H,8,9,10)&lt;/INCHI&gt;, &lt;SMILES&gt;CC1=CC=C(C=C1)S(=O)(=O)O&lt;/SMILES&gt;, &lt;IUPAC&gt;4-methylbenzenesulfonic acid&lt;/IUPAC&gt; to produce &lt;INCHI&gt;InChI=1S/C8H14O2/c1-7-4-3-5-8(2,10-7)9-6-7/h3-6H2,1-2H3/t7-,8+/m0/s1&lt;/INCHI&gt;, &lt;SMILES&gt;C\[C@@\]12CCC\[C@@\](O1)(OC2)C&lt;/SMILES&gt;, &lt;IUPAC&gt;(1S,5R)-1,5-dimethyl-6,8-dioxabicyclo\[3.2.1\]octane&lt;/IUPAC&gt;. X has chemical formula C10H22O4 and contains an acetal. Provide molecule X.

Think step by step and solve the problem below. At the end of your response, write your final answer on a new line starting with “FINAL ANSWER”. It should be an answer to the question such as providing a number, mathematical expression, formula, or entity name, without any extra commentary or providing multiple answer attempts.
```

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Identify molecule X (C10H22O4, containing an acetal) that undergoes p-toluenesulfonic acid-catalyzed cyclization to form the bicyclic acetal product (1S,5R)-1,5-dimethyl-6,8-dioxabicyclo[3.2.1]octane (C8H14O2).",
    "subtasks": [
      {
        "subtask": "Characterize the bicyclic product structure and deduce its connectivity",
        "atomics": [
          "Decode bicyclo[3.2.1] notation: 7-membered ring with 2-carbon bridge and 1-carbon bridge",
          "Map oxygen positions 6 and 8 to identify two ether linkages in the bicyclic core",
          "Locate 1,5-dimethyl substituents at bridgehead carbons with (1S,5R) stereochemistry",
          "Build full 3D structure of the product acetal"
        ]
      },
      {
        "subtask": "Determine molecular formula relationships and balance the cyclization reaction",
        "atomics": [
          "Compare X formula (C10H22O4) with product formula (C8H14O2)",
          "Calculate net atom loss: C2H8O2, consistent with two water molecules",
          "Determine that cyclization is intramolecular with acid catalysis and no external reagents",
          "Infer X has hydroxyl groups that condense under p-TsOH to form product ether oxygens"
        ]
      },
      {
        "subtask": "Identify functional groups in X capable of forming the bicyclic acetal",
        "atomics": [
          "Recognize X already contains an acetal functional group (given in problem)",
          "Determine X must have hydroxyl groups (4 oxygens total, multiple H in formula)",
          "Infer that cyclization requires properly positioned OH and acetal groups",
          "Map which X functional groups become the product's two ether oxygens"
        ]
      },
      {
        "subtask": "Apply retrosynthetic analysis to deduce X structure",
        "atomics": [
          "Disconnect the two ether bonds in product 6,8-positions to identify X precursor",
          "Trace carbons: product has 8 carbons (with 2 methyls), X has 10 carbons total",
          "Identify that X must be a C10 diol or polyol with an existing acetal moiety",
          "Reconstruct the C10 skeleton and position functional groups for cyclization"
        ]
      },
      {
        "subtask": "Propose candidate X structures and verify against all constraints",
        "atomics": [
          "Propose X is likely a diol or polyol with C10H22O4 formula containing a ketone acetal or diethyl acetal",
          "Verify that acid-catal
```

**Judge verdict + justification**:

`needs revision` — The gold_actions structure omits the global_atomics section present in the
hierarchy (3 cross-task verification steps are scattered into subtask 5 instead of separated), and
the gold_actions global statement incorrectly names the product as '1,4-dioxabicyclo[3.2.1]' when
the problem explicitly specifies '6,8-dioxabicyclo[3.2.1]octane'.

### Example 76: WorkArena++ (pilot_row_index=77)

**task_id**: `m2w_0790c8be-6e6d-4e2a-9c13-43ac9367da4c`\
**judge_verdict**: `acceptable`

**Input (annotator prompt user message)**:

```text
Benchmark: WorkArena++
Domain: web agent / Auto (Mind2Web proxy — WorkArena++ unavailable on HF)

Problem:
search the most recent full time Accounting & Finance Job available in Richmond, Virginia.
```

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Navigate a job search website, filter for full-time Accounting & Finance positions in Richmond, Virginia, sort by most recent posting, and extract the top job listing details.",
    "subtasks": [
      {
        "subtask": "Access and load a job search platform",
        "atomics": [
          "Open a web browser",
          "Navigate to a job search website (e.g., Indeed, LinkedIn)",
          "Wait for the job search page to fully load"
        ]
      },
      {
        "subtask": "Configure job search filters for the required criteria",
        "atomics": [
          "Enter 'Accounting & Finance' or 'Accountant' in the job title search field",
          "Enter 'Richmond, Virginia' in the job location field",
          "Select 'Full-time' from the employment type filter"
        ]
      },
      {
        "subtask": "Execute the search and organize results by posting date",
        "atomics": [
          "Submit the search query",
          "Wait for search results to load",
          "Sort results by 'Most Recent' or 'Date Posted' to show newest jobs first"
        ]
      },
      {
        "subtask": "Locate and validate the most recent job listing",
        "atomics": [
          "Examine the first result in the sorted list",
          "Verify the job title is Accounting & Finance related",
          "Verify the location is Richmond, Virginia",
          "Confirm employment type is Full-time",
          "Check the posting date to confirm it is the most recent"
        ]
      },
      {
        "subtask": "Retrieve and extract the job details",
        "atomics": [
          "Click on the top job listing to open the full job posting",
          "Extract and document: job title, company name, location, employment type, salary (if available), posting date, and job description"
        ]
      }
    ],
    "global_atomics": [
      "Verify the job posting is still active (not closed or expired)",
      "Confirm this is the absolute most recent full-time Accounting & Finance job in Richmond, Virginia by checking the posting date against other visible results"
    ]
  },
  "gold_actions": {
    "global": "Open Indeed or LinkedIn jobs, search 'Accounting & Finance', filter location to Richmond Virginia and employment type to Full-time, sort by most recent, and extract top result.",
    "subtasks": [
      {
        "subtask": "Load a major job search platform",
        "atomics": [
          "Open browser and navigate to
```

**Judge verdict + justification**:

`acceptable` — The global statement clearly captures the plan in one sentence; the five subtasks
(access platform, set filters, execute search, validate top result, extract details) together cover
all requirements of searching for the most recent full-time Accounting & Finance job in Richmond,
Virginia; the atomics are operational steps that execute in sequence to complete each subtask;
global_atomics contain only final verification steps that genuinely cross subtasks; and gold_actions
mirrors the same structure with appropriate platform-specific detail.

### Example 59: tau-bench (pilot_row_index=60)

**task_id**: `he_HumanEval_3`\
**judge_verdict**: `None`

**Input (annotator prompt user message)**:

```text
Benchmark: tau-bench
Domain: code generation (HumanEval proxy — tau-bench unavailable on HF)

Problem:
from typing import List


def below_zero(operations: List[int]) -> bool:
    """ You're given a list of deposit and withdrawal operations on a bank account that starts with
    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and
    at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    """
```

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Maintain running balance through operations and return True if balance ever goes below zero.",
    "subtasks": [
      {
        "subtask": "Initialize balance tracking variable",
        "atomics": [
          "Create balance variable initialized to zero"
        ]
      },
      {
        "subtask": "Iterate through operations and accumulate balance with negative detection",
        "atomics": [
          "Loop through each operation in the input list",
          "Update balance by adding the current operation value",
          "Check if updated balance is below zero",
          "Return True if negative balance is detected"
        ]
      },
      {
        "subtask": "Return False if no negative balance found",
        "atomics": [
          "Return False after loop completes without early exit"
        ]
      }
    ],
    "global_atomics": []
  },
  "gold_actions": {
    "global": "Accumulate operations sequentially and return True at first negative balance.",
    "subtasks": [
      {
        "subtask": "Initialize balance to 0",
        "atomics": [
          "balance = 0"
        ]
      },
      {
        "subtask": "Loop through operations, accumulate, and check for negative",
        "atomics": [
          "for operation in operations:",
          "balance += operation",
          "if balance < 0: return True"
        ]
      },
      {
        "subtask": "Return False as default",
        "atomics": [
          "return False"
        ]
      }
    ],
    "global_atomics": []
  }
}
```

### Example 40: SWE-bench Verified (pilot_row_index=40)

**task_id**: `swe_astropy__astropy-8707`\
**judge_verdict**: `None`

**Input (annotator prompt user message)**:

```text
Benchmark: SWE-bench Verified
Domain: astropy

Problem:
Header.fromstring does not accept Python 3 bytes
According to [the docs](http://docs.astropy.org/en/stable/_modules/astropy/io/fits/header.html#Header.fromstring), the method `Header.fromstring` "...creates an HDU header from a byte string containing the entire header data."

By "byte string" here it really means the `str` type which on Python 2 could be raw binary data, but on Python 3 explicitly is not.   In fact it does work on Python 3's unicode `str`s, but here it assumes that the data can be ASCII-encoded.

Its counterpart, `Header.fromfile` will work with files opened in text or binary mode.  So probably the simplest solution for now (as opposed to adding new methods or something like that) is to change `Header.fromstring` to accept unicode or bytes string types.

`Card.fromstring` likely needs a similar treatment.
```

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Make Header.fromstring and Card.fromstring accept both unicode str and bytes types by adding conditional decoding logic at method entry points.",
    "subtasks": [
      {
        "subtask": "Modify Card.fromstring to handle both str and bytes inputs",
        "atomics": [
          "Check if input is bytes type at method entry",
          "Decode bytes to str using ASCII encoding",
          "Handle decoding errors by attempting UTF-8 or raising ValueError",
          "Pass decoded string to existing parsing logic"
        ]
      },
      {
        "subtask": "Modify Header.fromstring to handle both str and bytes inputs",
        "atomics": [
          "Check if input is bytes type at method entry",
          "Decode bytes to str using ASCII encoding",
          "Handle decoding errors by attempting UTF-8 or raising ValueError",
          "Pass decoded string to existing Card iteration and parsing logic"
        ]
      },
      {
        "subtask": "Validate round-trip compatibility with file operations",
        "atomics": [
          "Read FITS header data from binary mode file handle",
          "Verify decoded bytes from binary read pass through fromstring",
          "Test Header.fromfile with both text and binary mode files",
          "Confirm existing fromfile behavior is preserved"
        ]
      },
      {
        "subtask": "Add test coverage for both input types",
        "atomics": [
          "Create test fixtures with valid FITS header in str and bytes format",
          "Write test for Card.fromstring accepting bytes input",
          "Write test for Header.fromstring accepting bytes input",
          "Write tests verifying str input behavior unchanged",
          "Write tests for decoding error cases"
        ]
      }
    ],
    "global_atomics": [
      "Run existing astropy.io.fits test suite to verify no regressions",
      "Verify documentation and docstrings accurately reflect both input types"
    ]
  },
  "gold_actions": {
    "global": "Add isinstance(input, bytes) checks with .decode('ascii') conversion in Card.fromstring and Header.fromstring, falling back to UTF-8 decode on failure.",
    "subtasks": [
      {
        "subtask": "Implement bytes handling in Card.fromstring",
        "atomics": [
          "Insert isinstance(cardstring, bytes) conditional at method start",
          "Call cardstring.decode('ascii') within try block",
          "Add except UnicodeDecodeError to attempt .decod
```

### Example 30: SWE-bench Verified (pilot_row_index=29)

**task_id**: `swe_pydata__xarray-6744`\
**judge_verdict**: `None`

**Input (annotator prompt user message)**:

````text
Benchmark: SWE-bench Verified
Domain: xarray

Problem:
"center" kwarg ignored when manually iterating over DataArrayRolling
### Discussed in https://github.com/pydata/xarray/discussions/6738

<div type='discussions-op-text'>

<sup>Originally posted by **ckingdon95** June 29, 2022</sup>
Hello, I am trying to manually iterate over a DataArrayRolling object, as described [here ](https://docs.xarray.dev/en/stable/user-guide/computation.html#rolling-window-operations)in the documentation.

I am confused why the following two code chunks do not produce the same sequence of values. I would like to be able to manually iterate over a DataArrayRolling object, and still be given center-justified windows. Is there a way to do this?

```python
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")

# Option 1: take a center-justified rolling average
result1 = my_data.rolling(x=3, center=True).mean().values
result1
````
This returns the following values, as expected:
```
array([nan,  2.,  3.,  4.,  5.,  6.,  7.,  8., nan])
```

Whereas when I do it manually, it is not equivalent:

```python
# Option 2: try to manually iterate, but the result is not centered
my_data_rolling = my_data.rolling(x=3, center=True)
result2 = [window.mean().values.item() for label, window in my_data_rolling]
result2
```
This returns
```
[nan, nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
```
Is this an issue with the window iterator? If it is not an issue, then is there a way for me to get
the center-jus ... [truncated for results doc; FULL text was passed to the model]
````

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Fix the DataArrayRolling iterator to respect the center parameter when manually iterating over windows.",
    "subtasks": [
      {
        "subtask": "Understand the current rolling window implementation and how centering is applied in reduction methods",
        "atomics": [
          "Read the DataArrayRolling class definition and __init__ method to understand center parameter storage",
          "Trace how the center parameter is used in reduction methods like .mean() to shift window boundaries",
          "Examine the internal window boundary calculation logic for both centered and non-centered cases",
          "Document the expected offset formula when center=True (typically ceil(window_size/2) or similar)"
        ]
      },
      {
        "subtask": "Identify why the __iter__ method ignores the center parameter",
        "atomics": [
          "Locate the __iter__ method in DataArrayRolling or parent BaseRolling class",
          "Compare window index calculation in __iter__ versus the reduction methods",
          "Verify that center parameter is stored in the rolling object but not applied during iteration",
          "Identify the exact point in the window generation code where the center offset should be applied"
        ]
      },
      {
        "subtask": "Implement centering logic in the rolling window iterator",
        "atomics": [
          "Modify __iter__ to compute the center offset when self.center=True",
          "Apply the offset to window start/end indices to shift windows appropriately",
          "Ensure iteration produces windows with correct alignment matching the direct reduction approach",
          "Handle boundary conditions where windows may be truncated at data edges"
        ]
      },
      {
        "subtask": "Add tests verifying manual iteration respects the center parameter",
        "atomics": [
          "Write test comparing manual iteration output with direct .mean() output for center=True",
          "Test multiple window sizes (3, 5, 7) and data lengths to ensure correctness",
          "Verify NaN placement and values match the expected centered pattern",
          "Test both centered and non-centered rolling to confirm both modes work"
        ]
      },
      {
        "subtask": "Validate the fix against existing functionality",
        "atomics": [
          "Run the existing rolling window test suite to detect any regressions",
          "Verify all rolling reduction
````

### Example 0: FrontierScience-Olympiad (pilot_row_index=0)

**task_id**: `fs_af50243e-3a60-4460-9536-f9a02c4f8eb8`\
**judge_verdict**: `None`

**Input (annotator prompt user message)**:

```text
Benchmark: FrontierScience-Olympiad
Domain: physics

Problem:
Context: Generalized (or weakened) quantum measurements introduce qualitatively new features in fundamental quantum physics that do not appear with simple projective measurements. Moreover, sequences of weak measurements can be made effectively continuous, resulting in quantum state evolutions described by quantum stochastic processes. Crucially, continuous quantum monitoring makes feedback control feasible, allowing parameters in the system Hamiltonian to be dynamically adjusted based on measurement outcomes.

In classical stochastic systems, an important class of problems involves rare-event physics, specifically processes characterized by unlikely transitions that start and end at specific points in phase space. In classical contexts, these rare events can be analyzed by introducing a canonical phase space formulation and identifying optimal paths by minimizing a suitable action functional under specified boundary conditions.

A comparable situation emerges in continuously measured quantum systems, where one seeks to prepare an initial quantum state and later observes a rare final (postselected) state at a specified time.

Here, we would like to develop a stochastic path integral formulation of continuous quantum measurements, deriving an action principle that naturally incorporates boundary conditions such as postselection. This formulation complements and generalizes the known stochastic Schrödinger or master equation approaches, recovering them as special cases when pos
... [truncated for results doc; FULL text was passed to the model]
```

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Develop a stochastic path integral framework for continuously measured quantum systems by doubling the state space to form a canonical quantum phase space, derive an action principle with postselection boundaries to identify optimal measurement trajectories, and apply this formalism to solid-state qubits to characterize rare quantum jump events in both measurement regimes and the quantum Zeno limit.",
    "subtasks": [
      {
        "subtask": "Formulate the stochastic path integral incorporating postselection as explicit boundary conditions",
        "atomics": [
          "Review Mensky's restricted path integral formulation for continuous measurement and identify how measurement operators induce path contraction",
          "Extend the path integral to include final-state projector |\u03c8f\u27e9 as hard boundary condition via modified functional measure",
          "Derive the effective action S_eff[\u03c8,\u03c8\u0304] from the path integral with preselection |\u03c8\u2080\u27e9 at t=0 and postselection |\u03c8f\u27e9 at t=T",
          "Verify that taking the limit where postselection\u2192identity operator recovers the standard stochastic Schr\u00f6dinger equation"
        ]
      },
      {
        "subtask": "Double the quantum state space to establish canonical quantum phase-space structure",
        "atomics": [
          "Define the extended Hilbert space H\u2297H* with forward-propagating fields \u03c8(t) and conjugate backward-propagating fields \u03c8\u0304(t)",
          "Establish canonical Poisson bracket relations {\u03c8(t), \u03c0\u0304(t')} = \u03b4(t\u2212t') in the extended phase space, verifying consistency with quantum measurement algebra",
          "Derive the stochastic action functional S = \u222b\u2080\u1d40 [\u03c8\u0304\u00b7\u2202_t \u03c8 \u2212 H_eff(\u03c8,\u03c8\u0304) + S_meas(\u03c8,\u03c8\u0304,dW)] dt from the path integral measure",
          "Demonstrate that extremization of S via \u03b4S/\u03b4\u03c8=0 and \u03b4S/\u03b4\u03c8\u0304=0 determines optimal trajectories connecting preselected and postselected states"
        ]
      },
      {
        "subtask": "Identify and characterize optimal trajectories by extremizing the stochastic action",
        "atomics": [
          "Write the explicit stochastic Hamiltonian H_eff(\u03c8,\u03c8\u0304) = \u03c8\u0304\u00b7H\u2080\u00b7\u03c8 + \u03b3_meas(\u03c8\u0304 M\u2020 M \u03c8 \u2212 |\u03c8\u0304|\u00b2\u27e8M\u2020M\u27e9)/2
```

### Example 7: FrontierScience-Olympiad (pilot_row_index=7)

**task_id**: `fs_d3acd2cb-8477-4630-b8bb-b4bc22670dc8`\
**judge_verdict**: `acceptable`

**Input (annotator prompt user message)**:

```text
Benchmark: FrontierScience-Olympiad
Domain: physics

Problem:
Context: For few-body system problems, a typical problem is to find the energy spectrum of a given quantum Hamiltonian. For example, let us consider the three-dimensional lattice Hamiltonian for a spin-1/2 non-relativistic nucleon. The Hamiltonian reads

 \\\[H = t\\sum\_{r,\\alpha, \\sigma} (2N^\\dagger\_{r,\\sigma}N\_{r,\\sigma} - N^\\dagger\_{r,\\sigma} N\_{r+e\_\\alpha,\\sigma} - N^\\dagger\_{r+e\_\\alpha,\\sigma} N\_{r,\\sigma}) + C\\times t \\sum\_{r} N^\\dagger\_{r,1}N^\\dagger\_{r,2}N\_{r,2}N\_{r,1}, \\\]

where \\(\\alpha = (x,y,z)\\), `\( e_\alpha \)` is the unit vector in the `\( \alpha \)`-th direction, and \\(t\\) is a coupling constant depending on the lattice spacing. The lattice model is constructed in the Fock space formulation, using nucleon annihilation and creation operators \\(n\_{r,\\alpha}\\) and \\(n^\\dagger\_{r,\\alpha}\\), where \\(r\\) is the lattice site on a periodic cubic spatial lattice with \\(L\\) sites in each direction and \\(\\alpha = 1,2,3,4\\) are the four flavors that label neutrons (\\(n\\)) and protons (\\(p\\)) with spin-half components \\(\\uparrow\\) and \\(\\downarrow\\). To specify, the nucleon field is given as

\\(N\_{r}=(n\_{r,\\uparrow},n\_{r,\\downarrow}, p\_{r,\\uparrow}, p\_{r,\\downarrow})^T \\).

To maintain the translational symmetry of the system, we employ the periodic boundary condition. The first step is to develop a notation to describe our multi-particle states. We first construct a complete basis of single partic
... [truncated for results doc; FULL text was passed to the model]
```

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Analyze a lattice Hamiltonian for nucleons by constructing second-quantization basis states, matching lattice parameters to continuum physics, and computing single- and two-particle energy spectra.",
    "subtasks": [
      {
        "subtask": "Define single-particle basis and construct two-body singlet states in second quantization",
        "atomics": [
          "Define single-particle basis as momentum eigenstates on cubic lattice with periodic boundary conditions",
          "Construct two-body singlet state for identical spin-1/2 nucleons using creation/annihilation operators",
          "Write singlet state explicitly in terms of neutron and proton operators with spin indices",
          "Verify antisymmetrization property under particle exchange and normalization"
        ]
      },
      {
        "subtask": "Derive lattice parameter t by matching free-particle energy between lattice and continuum",
        "atomics": [
          "Write dispersion relation for single particle on lattice with periodic boundary conditions",
          "Express continuum free-particle dispersion in finite periodic box using allowed momenta",
          "Equate lowest energy eigenvalue of lattice to lowest energy of continuum free particle",
          "Solve for t in terms of physical mass, box size, and lattice spacing"
        ]
      },
      {
        "subtask": "Calculate lowest non-zero single-particle energy numerically",
        "atomics": [
          "Substitute given values: L_phy = 3.4 fm, nucleon mass M = 1634 MeV, \u210fc = 197.3 MeV\u00b7fm",
          "Determine lattice spacing from continuum matching relation",
          "Evaluate single-particle dispersion at lowest non-zero momentum k_min = 2\u03c0/L_phy",
          "Convert energy result to MeV using natural units"
        ]
      },
      {
        "subtask": "Determine two-body coupling constant C from binding energy and compute first excited state",
        "atomics": [
          "Set up two-body Hamiltonian with singlet interaction in continuum limit",
          "Apply bound-state condition requiring binding energy of -17.8 MeV",
          "Solve for coupling constant C that satisfies the energy constraint",
          "Calculate energy of first excited state by solving scattering equation or finding next eigenstate"
        ]
      },
      {
        "subtask": "Find second excited state energy and determine its degeneracy",
        "atomics": [
          "Enumer
```

**Judge verdict + justification**:

`acceptable` — The decomposition clearly covers all five parts of the problem: part (a) maps to
subtask 1, parts (b)–(c) to subtasks 2–3, part (d) to subtask 4, and part (e) to subtask 5. Each
subtask contains operational atomic steps that, when executed in order, would complete the required
calculation. The global statement accurately summarizes the overall approach, and the gold_actions
appropriately instantiate the abstract atomic steps with explicit formulas (dispersion relations,
matching condition, bound-state condition) and numerical results (k_min, binding energies,
degeneracy counts) that resolve any methodological ambiguities.

### Example 17: FrontierScience-Olympiad (pilot_row_index=17)

**task_id**: `fs_eec8840a-2d00-4e70-b043-0da51bd1b288`\
**judge_verdict**: `needs revision`

**Input (annotator prompt user message)**:

```text
Benchmark: FrontierScience-Olympiad
Domain: chemistry

Problem:
Colorless gas `\( A \)` reacts with pungent-smelling, colored gas `\( B \)` when exposed to radiation. From this, poisonous liquid `\( X \)` is extracted. `\( X \)` reacts with water (`\( H_2O \)`) to form two strong acids in a 2:1 ratio. When barium chloride (`\( BaCl_2 \)`) is added to the resulting solution, a precipitate of `\( C \)` is obtained. Liquid `\( Y \)`, which contains the same elements as liquid `\( X \)`, is also known. If the molar mass ratio of `\( B \)` to `\( A \)` is 1.107 and that of `\( X \)` to `\( Y \)` is 1.134, identify compound `\( X \)`.

Think step by step and solve the problem below. At the end of your response, write your final answer on a new line starting with “FINAL ANSWER”. It should be an answer to the question such as providing a number, mathematical expression, formula, or entity name, without any extra commentary or providing multiple answer attempts.
```

**Output (annotator JSON)**:

```json
{
  "hierarchy": {
    "global": "Identify compound X by determining the reactant gases A and B, analyzing the two strong acids formed with water, verifying the isomer Y relationship, and confirming elemental composition.",
    "subtasks": [
      {
        "subtask": "Identify gases A and B using molar mass ratio and physical properties",
        "atomics": [
          "Calculate required molar mass of A given B:A ratio of 1.107",
          "Match colorless gas A with calculated molar mass (expect M \u2248 64)",
          "Match colored, pungent gas B with calculated molar mass (expect M \u2248 71)",
          "Verify A and B undergo radiation-catalyzed reaction to form liquid product"
        ]
      },
      {
        "subtask": "Determine liquid product X from radiation reaction of A and B",
        "atomics": [
          "Predict reaction mechanism under UV radiation or light exposure",
          "Identify the poisonous liquid product formed from A + B",
          "Verify X contains elements that can form two strong acids"
        ]
      },
      {
        "subtask": "Analyze hydrolysis reaction of X with water",
        "atomics": [
          "Write balanced equation for X + H\u2082O reaction",
          "Identify the two strong acids formed and verify their molar ratio is 2:1",
          "Check that one acid is H\u2082SO\u2084 (to explain BaCl\u2082 precipitate C = BaSO\u2084)"
        ]
      },
      {
        "subtask": "Identify isomer Y and verify molar mass ratio",
        "atomics": [
          "Identify compound Y containing same elements as X but different formula",
          "Calculate molar mass ratio X:Y and verify it equals 1.134",
          "Confirm both X and Y are stable, known compounds"
        ]
      },
      {
        "subtask": "Verify precipitate formation and compound stability",
        "atomics": [
          "Write equation for BaCl\u2082 + reaction solution \u2192 precipitate C",
          "Confirm C is white precipitate (BaSO\u2084) from the strong acids",
          "Verify X is poisonous liquid at room temperature"
        ]
      }
    ],
    "global_atomics": [
      "Cross-check all molar mass calculations against known atomic masses",
      "Confirm compound X is recognized in chemistry literature with appropriate toxicity/properties",
      "Verify the chemical formulas and equations balance correctly"
    ]
  },
  "gold_actions": {
    "global": "Using molar mass 1.107 ratio and chemical properties, identify SO\u2
```

**Judge verdict + justification**:

`needs revision` — The gold_actions does not mirror the v2 structure: v2 specifies three
global_atomics (cross-check calculations, confirm literature recognition, verify equation balancing)
while gold_actions shows an empty global_atomics list, violating the structural correspondence
requirement.
