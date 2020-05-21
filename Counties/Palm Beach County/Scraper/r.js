const puppeteer = require("puppeteer-extra")
const pluginStealth = require("puppeteer-extra-plugin-stealth")
const csvWriter = require('csv-write-stream')
const fs = require('fs')
// end requires

const RecaptchaPlugin = require('puppeteer-extra-plugin-recaptcha')
const recaptchaPlugin = RecaptchaPlugin({
  provider: { id: '2captcha', token: 'Your token', throwOnError: true }
})

const writer = csvWriter({headers:[
    'CaseNum',
    'FirstName',
    'MiddleName',
    'LastName',
    'Suffix',
    'DOB',
    'Race',
    'Sex',
    'ArrestDate',
    'FilingDate',
    'OffenseDate',
    'DivisionName',
    'CaseStatus',
    'DefenseAttorney',
    'PublicDefender',
    'Judge',
    'Chargei will have to check it outCount',
    'ChargeStatute',
    'ChargeDescription',
    'ChargeDispoyou should see itsition',
    'ChargeDispositionDate',
    'ChargeOffenseDate',
    'ChargeCitationNum',
    'ChargePlea',
    'ChargePleaDate',
  ]})
writer.pipe(fs.createWriteStream('out-traffic.csv',{flags:'a'}))

puppeteer.use(recaptchaPlugin)
puppeteer.use(pluginStealth())

const datemaker = (days=0) => {
  let date = new Date(new Date().setDate(new Date().getDate() - days));
  return `${date.getMonth()+1}-${date.getDate()}-${date.getFullYear()}`
}

// 2827 was the biggest before i found out it was skipping a day

let settings = {
  pages: 6000,
  days: 1,
  start: 3587,
  end: 3587,
  timeout: 60000
}

puppeteer.launch({ headless: false,})
  .then(async browser => {
    const page = await browser.newPage()
    page.setDefaultNavigationTimeout(settings.timeout)
    await page.setViewport({ width: 1280, height: 1024 })
    await page.goto("https://applications.mypalmbeachclerk.com/eCaseView/LandingPage.aspx")
    await page.click("#cphBody_ibGuest")
    if (await page.$('.g-recaptcha') !== null) {
      try {
        await page.solveRecaptchas()
        await Promise.all([
          page.click('input[id="cphBody_cmdContinue"]')
        ])
      }
      catch {
        await page.solveRecaptchas()
        await Promise.all([
          page.click('input[id="cphBody_cmdContinue"]')
        ])
      }
    }
    if (await page.$('.g-recaptcha') !== null) {
      try {
        await page.solveRecaptchas()
        await Promise.all([
          page.click('input[id="cphBody_cmdContinue"]')
        ])
      }
      catch {
        await page.solveRecaptchas()
        await Promise.all([
          page.click('input[id="cphBody_cmdContinue"]')
        ])
      }
    }
    await page.waitFor('select[name="ctl00$cphBody$gvSearch$ctl11$cmbParameterPostBack"]')
    await page.select('select[name="ctl00$cphBody$gvSearch$ctl11$cmbParameterPostBack"]', '8')
    for(let iteration = 0; iteration < settings.pages; iteration++){
	    console.log(settings.start)
	    await page.waitFor('input[name="ctl00$cphBody$gvSearch$ctl08$txtParameter"]')
	    await page.focus('input[name="ctl00$cphBody$gvSearch$ctl08$txtParameter"]')
	    await page.keyboard.down('Control');
	    await page.keyboard.press('A');
	    await page.keyboard.up('Control');
	    await page.keyboard.press('Backspace');
	    await page.keyboard.type(datemaker(settings.start))
	    await page.waitFor('input[name="ctl00$cphBody$gvSearch$ctl07$txtParameter"]')
	    await page.focus('input[name="ctl00$cphBody$gvSearch$ctl07$txtParameter"]')
	    await page.keyboard.down('Control');
	    await page.keyboard.press('A');
	    await page.keyboard.up('Control');
	    await page.keyboard.press('Backspace');
	    await page.keyboard.type(datemaker(settings.end))
	    await page.waitFor('input[name="ctl00$cphBody$cmdSearch"]')
	    await page.click('input[name="ctl00$cphBody$cmdSearch"]')
	    await page.waitFor('select[name="ctl00$cphBody$cmbPageSize"]')
	    await page.select('select[name="ctl00$cphBody$cmbPageSize"]', 'All')
	    await page.waitFor('td[align="left"] > a')
	    // initial collection for # of records

	    const records = await page.$$('td[align="left"] > a')
	    for (let i = 0; i < records.length; i++) {
	      // get all records
	      await page.waitFor('select[name="ctl00$cphBody$cmbPageSize"]')
	      await page.select('select[name="ctl00$cphBody$cmbPageSize"]', 'All')
	      await page.waitFor('td[align="left"] > a')
	      await page.waitFor(750)
	      const recordsInner = await page.$$('td[align="left"] > a')
	      await page.waitFor(750)
	      await recordsInner[i].click()
	      // ENTER record
	      try {
	        await page.waitFor('tr', {timeout: 4000})
	      }
	      catch{
	        if (await page.$('.g-recaptcha') !== null) {
	          await page.solveRecaptchas()
	          await Promise.all([
	            page.click('input[id="cphBody_cmdContinue"]')
	          ])
	          await page.waitFor('tr')
	        }
	      }
	      const caseInfo = await page.$$('tr')
	      // initiate what we're about to write to CSVs
	      const caseArray = []
	      await page.waitFor('#cphBody_lblCaseNumber')
	      const caseNum = await page.$eval('#cphBody_lblCaseNumber', e => e.innerText.replace('CASE NUMBER: ', '').replace(/-/g, ''))
	      caseArray.push(caseNum)

	      for (let x = 0; x < caseInfo.length; x++) {
	        let label = await caseInfo[x].$$('td')
	        let labelValue = await label[1].getProperty('textContent')
	        await caseArray.push(labelValue._remoteObject.value)
	      }


	      // go to Party Names - if party type == DEFENSE ATTORNEY then collect name
	      // PARTY NAMES COLLECTION START
	      await page.waitFor('#cphBody_lbParties')
	      await page.click('#cphBody_lbParties')
	      await page.waitFor(500)
	      try { await page.waitFor('tr', { timeout: 4000 }) }
	      catch{ await page.waitFor('tr') }
	      const partyNames = await page.$$('tr')

	      let defenseattorney = []
	      let publicdefender = []
	      let judge = []

	      for (let x = 1; x < partyNames.length; x++) {
	        let label = await partyNames[x].$$('td')
	        // get the first name
	        let labelValue = await label[0]
	        let label0 = await labelValue.getProperty('textContent')
	        // get the middle name
	        let fn1 = await label[1]
	        let label1 = await fn1.getProperty('textContent')
	        // get the last name
	        let fn2 = await label[2]
	        let label2 = await fn2.getProperty('textContent')
	        // // get the party type
	        let fn3 = await label[8]
	        let label3 = await fn3.getProperty('textContent')
	        if (label3._remoteObject.value == "DEFENSE ATTORNEY") {
	          let fullname = (label0._remoteObject.value + ' ' + label1._remoteObject.value + ' ' + label2._remoteObject.value).replace(/\s{2,}/,' ')

	          defenseattorney.push(fullname)
	        }
	        if (label3._remoteObject.value == "PUBLIC DEFENDER") {
	          let fullname = (label0._remoteObject.value + ' ' + label1._remoteObject.value + ' ' + label2._remoteObject.value).replace(/\s{2,}/,' ')
	          publicdefender.push(fullname)
	        }
	        if (label3._remoteObject.value == "JUDGE") {
	          let fullname = (label0._remoteObject.value + ' ' + label1._remoteObject.value + ' ' + label2._remoteObject.value).replace(/\s{2,}/,' ')
	          judge.push(fullname)
	        }
	      }
	      // Convert arrays to string and push them to row array
	      await caseArray.push(defenseattorney.toString(), publicdefender.toString(), judge.toString())
	      // PARTY NAMES COLLECTION END


	      // CHARGES COLLECTION START
	      await page.waitFor('#cphBody_liCharges')
	      await page.click('#cphBody_liCharges')
	      await page.waitFor(500)
	      await page.waitFor('#cphBody_gvCharges tr')
	      let charges = await page.$$('#cphBody_gvCharges tr');
	      // while loop time

	      let chargeRecordStart = 1;
	      let chargeNumPages = 2;
	      let chargeCurrentPage = 1;
	      let chargePages = 0

	      try {
	        await page.waitFor('.pagination-ys', {timeout: 500});
	        chargePages = await page.$$('.pagination-ys td');
	        chargeNumPages = chargePages.length;
	        chargeRecordStart = 3;
	      }
	      catch {}
	      for (let y = 1; y < chargeNumPages; y++){
	        if (y > 1) {
	          chargePages = await page.$$('.pagination-ys td');
	          await chargePages[y].click()
	          await page.waitFor('#cphBody_gvCharges tr')
	          charges = await page.$$('#cphBody_gvCharges tr');
	        }
	        for (let x = chargeRecordStart; x < charges.length; x++) {

	          let chargetd = await charges[x].$$('td')

	          // Collect charge count
	          let chargeItem0 = await chargetd[0]
	          let charge0 = await chargeItem0.getProperty('textContent')
	          // Collect charge statute
	          let chargeItem1 = await chargetd[1]
	          let charge1 = await chargeItem1.getProperty('textContent')
	          // Collect charge description
	          let chargeItem2 = await chargetd[2]
	          let charge2 = await chargeItem2.getProperty('textContent')
	          // Collect charge diposition
	          let chargeItem3 = await chargetd[3]
	          let charge3 = await chargeItem3.getProperty('textContent')
	          // Collect charge disposition date
	          let chargeItem4 = await chargetd[4]
	          let charge4 = await chargeItem4.getProperty('textContent')
	          // Collect charge offense date
	          let chargeItem5 = await chargetd[5]
	          let charge5 = await chargeItem5.getProperty('textContent')
	          // Collect charge citation number
	          let chargeItem6 = await chargetd[6]
	          let charge6 = await chargeItem6.getProperty('textContent')
	          // Collect charge plea
	          let chargeItem7 = await chargetd[7]
	          let charge7 = await chargeItem7.getProperty('textContent')
	          // Collect charge plea date
	          let chargeItem8 = await chargetd[8]
	          let charge8 = await chargeItem8.getProperty('textContent')

	          // Let's make things nice and put them into an array just so we can unpack it on the next line, lol
	          let chargeArray = [charge0._remoteObject.value,charge1._remoteObject.value,charge2._remoteObject.value,charge3._remoteObject.value,charge4._remoteObject.value,charge5._remoteObject.value,charge6._remoteObject.value,charge7._remoteObject.value,charge8._remoteObject.value]

	          // Write each charge as a row
	          await writer.write([...caseArray, ...chargeArray])
	        }
	      }
	      // CHARGES COLLECTION END



	      // EXIT record
	      await page.waitFor('li[id="cphBody_liResults"]')
	      await page.click('li[id="cphBody_liResults"]')
	    }
        await page.waitFor('li[id="cphBody_liSearch"]')
        await page.click('li[id="cphBody_liSearch"]')
        settings.start += settings.days
        settings.end += settings.days
    }
    await writer.end()
    await browser.close()
  })
