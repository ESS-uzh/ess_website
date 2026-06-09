const projects = window.projects;

const nodes = [];
const edges = [];

const tagSet = new Set();
const regionSet = new Set();
const researcherSet = new Set();

projects.forEach(project => {

    // PROJECT NODE

    nodes.push({
        data: {
            id: `project-${project.id}`,
            label: project.name,
            type: 'project'
        }
    });

    // REGION

    if (project.region) {

        const regionId = `region-${project.region}`;

        if (!regionSet.has(regionId)) {

            regionSet.add(regionId);

            nodes.push({
                data: {
                    id: regionId,
                    label: project.region,
                    type: 'region'
                }
            });
        }

        edges.push({
            data: {
                source: `project-${project.id}`,
                target: regionId
            }
        });
    }

    // TAGS

    (project.tags || []).forEach(tag => {

        const tagId = `tag-${tag}`;

        if (!tagSet.has(tagId)) {

            tagSet.add(tagId);

            nodes.push({
                data: {
                    id: tagId,
                    label: tag,
                    type: 'tag'
                }
            });
        }

        edges.push({
            data: {
                source: `project-${project.id}`,
                target: tagId
            }
        });

    });

    // RESEARCHERS

    (project.participants || []).forEach(person => {

        const researcherId =
            `researcher-${person.name}`;

        if (!researcherSet.has(researcherId)) {

            researcherSet.add(researcherId);

            nodes.push({
                data: {
                    id: researcherId,
                    label: person.name,
                    type: 'researcher'
                }
            });
        }

        edges.push({
            data: {
                source: `project-${project.id}`,
                target: researcherId
            }
        });

    });

});

const cy = cytoscape({

    container: document.getElementById('project-universe'),

    elements: [
        ...nodes,
        ...edges
    ],

    style: [

        {
            selector: 'node[type="project"]',
            style: {
                'label': 'data(label)',
                'width': 40,
                'height': 40
            }
        },

        {
            selector: 'node[type="tag"]',
            style: {
                'shape': 'rectangle',
                'label': 'data(label)'
            }
        },

        {
            selector: 'node[type="region"]',
            style: {
                'shape': 'triangle',
                'label': 'data(label)'
            }
        },

        {
            selector: 'node[type="researcher"]',
            style: {
                'shape': 'diamond',
                'label': 'data(label)'
            }
        },

        {
            selector: 'edge',
            style: {
                'width': 1
            }
        }

    ],

    layout: {
        name: 'cose',
        animate: true
    }

});